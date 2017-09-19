# Miscellaneous login utilities
bowser = require 'bowser'
context = require './context'

# Get current login from localstorage
loginKey = "v3.login"
exports.getLogin = (storage) ->
  if storage.get(loginKey)
    return JSON.parse(storage.get(loginKey))
  return null

# Set current login from localstorage 
exports.setLogin = (storage, login) ->
  if login?
    storage.set(loginKey, JSON.stringify(login))
  else if storage.get(loginKey)
    storage.remove(loginKey)

exports.login = (username, password, loginToken, ctx, success, error) ->
  console.log "Logging in as: #{username}"

  url = ctx.apiUrl + 'clients'
  req = $.ajax(url, {
    data : JSON.stringify({
      username: username
      password: password
      loginToken: loginToken
      version: @version
      domain: ctx.branding.domain
      appName: ctx.branding.title
    }),
    contentType : 'application/json',
    type : 'POST'})

  req.done (data, textStatus, jqXHR) =>
    response = JSON.parse(jqXHR.responseText)

    # Login 
    exports.setLogin(ctx.storage, response)

    # Update context, first stopping old one
    ctx.stop()
    context.setupLoginContext response, ctx, =>
      success()

  req.fail (jqXHR, textStatus, errorThrown) =>
    console.error "Login failure: #{jqXHR.responseText} (#{jqXHR.status})"
    if jqXHR.status < 500 and jqXHR.status >= 400 and jqXHR.status != 404 # 404 means no connection sometimes
      alert(JSON.parse(jqXHR.responseText).error)
    else
      alert(T("Unable to login. Please check that you are connected to Internet"))
    error()

# Performs a social login, redirecting as appropraite
exports.socialLogin = (ctx, provider) ->
  # First check connectivity
  $.get(ctx.apiUrl + "ping").done () =>
    # If in Phonegap/Cordova, we can't redirect back to the file:/// url that runs the app
    # as the browser blocks local redirects. Instead, we need to run an InAppBrowser
    # that goes to the API's signin page and then catch the redirect via an event handler
    if window.cordova
      # Fake URL to catch on redirect
      loginTokenUrl = "http://mwater.co/#social_data/SOCIAL_DATA" 
      socialLoginUrl = ctx.apiUrl + "auth/#{provider}?destUrl=" + encodeURIComponent(loginTokenUrl)

      inAppBrowser = window.open(socialLoginUrl, "_blank", "location=no")
      inAppBrowser.addEventListener 'loadstart', (event) => 
        # Check for fictional redirect
        if event.url.match(/http:\/\/mwater\.co/)
          console.log event.url
          # Get social data
          socialDataStr = event.url.match(/#social_data\/(.+)/)[1]

          # Close browser
          inAppBrowser.close()

          exports.handleSocialData(ctx, socialDataStr)
    else
      # Perform a social login with specified provider ("google", "facebook", etc.) 
      # Redirect to self with login token in hash
      loginTokenUrl = window.location.href.split("#")[0] + "#social_data/SOCIAL_DATA";
      socialLoginUrl = ctx.apiUrl + "auth/#{provider}?destUrl=" + encodeURIComponent(loginTokenUrl)
      window.location.href = socialLoginUrl
  .fail ()=>
    alert(T("Unable to sign in. Please check that you are connected to Internet"))

exports.socialLoginAvailable = ->
  # InappBrowser broken on Cordova Android 2.3
  if window.cordova and bowser.browser.android and bowser.browser.osversion.match(/^2\./)
    return false

  return true

# Commented out due to HomePage reference
# exports.handleSocialData = (ctx, socialDataStr) ->
#   # Get social data (unescape and parse)
#   socialData = {}
#   try 
#     socialData = JSON.parse(decodeURIComponent(decodeURIComponent(socialDataStr)))
#   catch ex
#     # Ignore as bad login
#     console.log "Social Data String: " + socialDataStr

#   # If login token present, use it
#   if socialData.loginToken
#     success = =>
#       HomePage = require './pages/HomePage'
#       ctx.pager.closeAllPages(HomePage)
#       ctx.pager.flash T("Login as {0} successful", ctx.login.user), "success"

#     error = => 
#       ctx.pager.flash T("Login failed"), "danger"
#       return

#     exports.login(null, null, socialData.loginToken, ctx, success, error)
#   else
#     # Open signup screen
#     SignupPage = require './pages/SignupPage'
#     ctx.pager.openPage(SignupPage, { socialData: socialData })

# Confirms the user's age is over 13
exports.confirmAge = (ctx, success, error) ->
  url = ctx.apiUrl + "users/#{ctx.login.user}?client=#{ctx.login.client}"
  req = $.ajax(url, {
    data : JSON.stringify({ ageConfirmed: true })
    contentType : 'application/json',
    type : 'POST'})
  req.done ->
    ctx.login.ageConfirmed = true
    success()
  req.fail ->
    error()

exports.logout = (ctx) ->
  # Logout
  exports.setLogin(ctx.storage, null)

  # Update context, first stopping old one
  ctx.stop()
  context.setupAnonymousContext ctx, =>
    ctx.pager.closeAllPages(require("./pages/LoginPage"))

