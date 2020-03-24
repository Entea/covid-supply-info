const { Text, Checkbox, Slug, Location, Integer } = require('@keystonejs/fields');

const GoogleMapsKey = process.env.GOOGLE_API_KEY

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
      googleMapsKey: GoogleMapsKey,
      label: 'Адрес учреждения'
    },
    phone: {
      type: Text,
      label: 'Номер телефона'
    },
    email: {
      type: Text,
      label: 'E-mail'
    }
  }
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
  AddressNodeSchema
};
