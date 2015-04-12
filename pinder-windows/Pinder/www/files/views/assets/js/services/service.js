/*
 * Service settings
 */
var Facebook_Settings = {
    "client_id": "702303806446281",
    "project_id": "33f72e88-f312-4e6d-866f-186e1004cd5b"
}

/*
 * Services
 */

var GetMeService = new Apperyio.RestService({
    'url': 'https://api.appery.io/rest/1/proxy/tunnel',
    'proxyHeaders': {
        'appery-proxy-url': 'http://ec2-54-211-26-30.compute-1.amazonaws.com/api/me',
        'appery-transformation': 'checkTunnel',
        'appery-key': '1428811739469',
        'appery-rest': 'fbb23d7d-56d3-4e0e-9b88-e43735365935'
    },
    'dataType': 'json',
    'type': 'get',
});

var SMSService = new Apperyio.RestService({
    'url': 'https://api.appery.io/rest/1/proxy/tunnel',
    'proxyHeaders': {
        'appery-proxy-url': 'http://ec2-54-211-26-30.compute-1.amazonaws.com/api/sms/',
        'appery-transformation': 'checkTunnel',
        'appery-key': '1428811739469',
        'appery-rest': 'fbb23d7d-56d3-4e0e-9b88-e43735365935'
    },
    'dataType': 'json',
    'type': 'post',
    'contentType': 'application/x-www-form-urlencoded',
});

var Facebook_MeService = new Apperyio.RestService({
    'url': 'https://graph.facebook.com/me',
    'dataType': 'json',
    'type': 'get',

    'serviceSettings': Facebook_Settings
});

var GetNearbyService = new Apperyio.RestService({
    'url': 'https://api.appery.io/rest/1/proxy/tunnel',
    'proxyHeaders': {
        'appery-proxy-url': 'http://ec2-54-211-26-30.compute-1.amazonaws.com/api/nearby',
        'appery-transformation': 'checkTunnel',
        'appery-key': '1428811739470',
        'appery-rest': 'fbb23d7d-56d3-4e0e-9b88-e43735365935'
    },
    'dataType': 'json',
    'type': 'get',
});
var GeolocationService = new Apperyio.GeolocationService({});

var GetNearbyAddressService = new Apperyio.RestService({
    'url': 'https://api.appery.io/rest/1/proxy/tunnel',
    'proxyHeaders': {
        'appery-proxy-url': 'http://ec2-54-211-26-30.compute-1.amazonaws.com/nearby/location',
        'appery-transformation': 'checkTunnel',
        'appery-key': '1428811739470',
        'appery-rest': 'fbb23d7d-56d3-4e0e-9b88-e43735365935'
    },
    'dataType': 'json',
    'type': 'get',
});