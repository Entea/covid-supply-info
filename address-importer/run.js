const {config} = require('dotenv');
const EasySoap = require('easysoap');
const fetch = require("node-fetch");

config();
const token = process.env.TOKEN;
const url = process.env.URL || 'http://localhost:3000/admin/api';

async function main() {
    const soapClient = EasySoap({
        host: 'address.darek.kg',
        path: '/ws/AddressApi',
        wsdl: '/ws/AddressApi',
        headers: {token},
        rejectUnauthorized: true / false
    }, {secure: false});

    const functions = await soapClient.getAllFunctions();
    console.log(functions);

    const topLevel = await soapClient.call({
        method: 'getOblastLevelUnits', params: {}
    });

    const rows = topLevel.data.getOblastLevelUnitsResponse.return.item;
    let subItems = [];

    for (const row of rows) {
        const treeGenerator = fetchChildren(soapClient, row.id);
        for await (const node of treeGenerator) {
            console.log(node);

            const result = await toGraphqlMutation(node);
            console.log(result)
        }
    }
    console.log(subItems);
}

async function * fetchChildren(soapClient, rowId) {
    const children = await soapClient.call({
        method: 'getChildren', params: {parent: rowId}
    });

    if (children.data.getChildrenResponse.return) {
        let array = children.data.getChildrenResponse.return.item;

        if (array.length > 0) {
            for (let i = 0; i < array.length; i++) {
                array[i].parentId = parseInt(rowId);
                array[i].addressId = parseInt(array[i].id);
                array[i].type = parseInt(array[i].type);

                let id = array[i].id;
                delete array[i].id;
                delete array[i].nameEn;

                yield array[i];
                yield * fetchChildren(soapClient, id);
            }
        }
    }
}

async function toGraphqlMutation(data) {
    return await fetchMutation(`mutation CreateNode($data: AddressNodeCreateInput) { 
        createAddressNode(data: $data) { id }
    }`, {data});
}

main()
    .then((r) => {
        console.log('Success', r);
    })
    .catch(e => {
        console.error('Error', e);
    });


async function fetchMutation(mutation, variables = null) {
    try {
        let body = {query: mutation};
        if (variables) {
            body.variables = variables;
        }

        const result = await fetch(`${url}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(body)
        });

        const json = await result.json();
        if (json.errors && json.errors.length > 0) {
            // noinspection ExceptionCaughtLocallyJS
            throw new Error(JSON.stringify(json));
        }

        if (json.data) {
            return json.data;
        }
    } catch (e) {
        console.error('error running mutation with variables', mutation, variables, e);
        throw e;
    }
}
