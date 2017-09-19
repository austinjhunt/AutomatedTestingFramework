_ = require 'lodash'
moment = require 'moment'
ImagePage = require './pages/ImagePage'
handlebars = require("hbsfy/runtime")
moment = require 'moment'

# Gets all properties that apply to a a given type
exports.getProperties = (properties, entityTypeCode, propCodes) ->
  if propCodes
    return _.map(propCodes, (pcode) -> _.findWhere(properties, { entity_type: entityTypeCode, code: pcode }))
  else
    return _.sortBy(_.where(properties, { entity_type: entityTypeCode }), "id")

exports.getEntityType = (entityTypes, entityTypeCode) ->
  return _.findWhere(entityTypes, { code: entityTypeCode })

exports.getProperty = (properties, entityTypeCode, propertyCode) ->
  return _.findWhere(properties, { entity_type: entityTypeCode, code: propertyCode })

exports.getUnit = (units, unitCode) ->
  return _.findWhere(units, { code: unitCode })

# Determine if can edit an entity
exports.canEdit = (entity, user, groups) ->
  roleIds = ["all", "user:#{user}"].concat(_.map(groups, (g) -> "group:" + g))

  # Can only edit if has admin or edit role
  return _.some entity._roles, (role) ->
    if role.to in roleIds and role.role in ['admin', 'edit']
      return true
    return false

# Determine if can remove an entity
exports.canRemove = (entity, user, groups) ->
  roleIds = ["all", "user:#{user}"].concat(_.map(groups, (g) -> "group:" + g))

  # Can only remove if has admin role
  return _.some entity._roles, (role) ->
    if role.to in roleIds and role.role in ['admin']
      return true
    return false

# Converts a localized string (e.g. { _base: "en", en: "Site", es: "Sitio" }) to a string
exports.localizeString = (localizedString, locale="en") ->
  # Null is ""
  if not localizedString
    return ""

  # Return locale if present
  if localizedString[locale]
    return localizedString[locale]

  # If English present, run it through T()
  if localizedString.en
    return T(localizedString.en)

  # Fall back to base
  return localizedString[localizedString._base] or ""

exports.createHandlebarsHelpers = (ctx) ->
  propertyName = (property) ->
    return property.name.en

  propertyValue = (entity, property) ->
    val = entity[property.code]
    if not val?
      return ""

    switch property.type
      when "text", "decimal", "integer"
        return val
      when "date"
        # If only date, simple format
        if val.length <= 10
          return moment(val).format("LL")
        else
          return moment(val).format("LLL")
      when "measurement"
        # Lookup units
        unit = exports.getUnit(val.unit)
        return val.magnitude + " " + (if unit then unit.symbol)
      when "enum"
        # Lookup value
        value = _.findWhere(property.values, code: val)
        return value.name.en
      when "boolean"
        return (if val then "Yes" else "No")
      when "image"
        # Create html that will have image loaded once thumbnail is obtained
        html = '''<img class="img-thumbnail image" id="img_''' + val.id + '''" src="img/image-loading.png" style="max-height: 160px" onError="this.onerror=null;this.src='img/no-image-icon.jpg';" />'''

        # Defer to allow html to render
        _.defer () =>
          success = (url) =>
            $("#img_#{val.id}").attr("src", url).on("click", => ctx.pager.openPage(ImagePage, { id: val.id}))

          error = =>
            # Display this image on error
            $("#img_#{val.id}").attr("src", "img/no-image-icon.jpg")

          ctx.imageManager.getImageThumbnailUrl(val.id, success, error)

        return new handlebars.SafeString(html)
      when "imagelist"
        # Create html that will have image loaded once thumbnail is obtained
        html = '<div>'
        for img in val
          do (img) =>
            html += '''<img class="img-thumbnail image" id="img_''' + img.id + '''" src="img/image-loading.png" style="max-height: 160px" onError="this.onerror=null;this.src='img/no-image-icon.jpg';" />'''
    
            # Defer to allow html to render
            _.defer () =>
              success = (url) =>
                $("#img_#{img.id}").attr("src", url).on("click", => ctx.pager.openPage(ImagePage, { id: img.id}))

              error = =>
                # Display this image on error
                $("#img_#{img.id}").attr("src", "img/no-image-icon.jpg")

              ctx.imageManager.getImageThumbnailUrl(img.id, success, error)

        html += '</div>'
        return new handlebars.SafeString(html)

  return { propertyName: propertyName, propertyValue: propertyValue }
