const {Relationship, Text, Virtual, Slug, Location, Integer, Select} = require('@keystonejs/fields');
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
      needs: {
          type: Relationship,
          ref: 'Need.clinic',
          many: true
      },
      location: {
          type: Location,
          googleMapsKey: GoogleMapsKey
      }
  }
};

const NeedSchema = {
    fields: {
        count: {
            type: Integer,
            isRequired: true,
            label: 'Количество'
        },
        needType: {type: Relationship, ref: 'NeedType'},
        clinic: {type: Relationship, ref: 'Clinic.needs'},
    },
    labelResolver: item => {
      return `${item['needType']} (${item.needType}) - ${item.count} в ${item.clinic}`
    }
};

const NeedTypeSchema = {
    fields: {
        name: {
            type: Text,
            isRequired: true,
            label: 'Наименование'
        },
        unit: {
            type: Text,
            isRequired: true,
            label: 'Единица измерения',
        }
    },
    labelResolver: item => `${item.name} (${item.unit})`,
};

const AddressNodeSchema = {
    fields: {
        addressId: {
            type: Integer,
            isRequired: true,
            label: 'Идентификатор в адресном реестре'
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
        location: {
            // Поле можно заполнить позже
            type: Location,
            googleMapsKey: GoogleMapsKey
        },
        parentId: {
            type: Integer,
            isRequired: true,
            label: 'Родительский узел в адресном реестре'
        }
    }
};

// Write more lists
// Learn about lists here https://www.keystonejs.com/tutorials/add-lists
// API reference here https://www.keystonejs.com/keystonejs/fields/

module.exports = {
    ClinicSchema,
    AddressNodeSchema,
    NeedSchema,
    NeedTypeSchema
};
