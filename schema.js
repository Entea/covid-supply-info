const { Text, Checkbox, Slug, Location } = require('@keystonejs/fields');

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
}

const OtherSchema = {
  /// ... write your schema fields e.t.c.
}

// Write more lists
// Learn about lists here https://www.keystonejs.com/tutorials/add-lists
// API reference here https://www.keystonejs.com/keystonejs/fields/

module.exports = {
  ClinicSchema,
  OtherSchema
}
