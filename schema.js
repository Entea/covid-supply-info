const { Text, Checkbox, Slug, Location, Integer } = require('@keystonejs/fields');

const GoogleMapsKey = "AIzaSyDlGeu3w8Sy1VbEPmEV8ved8V34aszwIyU"

const ClinicSchema = {
  fields: {
    name: {
      type: Text,
      isRequired: true,
      label: 'Название учреждения'
    },
    url: {
      type: Slug,
      isRequired: true,
      label: 'URL'
    },
    location: {
      type: Location,
      googleMapsKey: GoogleMapsKey
    }
  }
};

const AddressNodeSchema = {
    fields: {
        id: {
            type: Integer,
            isRequired: true,
            label: 'Идентификатор'
        },
        nameRu: {
            type: Text,
            label: 'Название'
        },
        nameKg: {
            type: Text,
            label: 'Аталышы'
        },
        ikaoA3: {
            type: Text
        },
        type: {
            type: Integer,
            label: 'Тип адреса'
        },
        typeKg: {
            type: Text
        },
        typeKgShort: {
            type: Text
        },
    }
};

// Write more lists
// Learn about lists here https://www.keystonejs.com/tutorials/add-lists
// API reference here https://www.keystonejs.com/keystonejs/fields/

module.exports = {
  ClinicSchema,
  AddressNodeSchema
};
