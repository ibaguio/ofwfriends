/**
 * Data models
 */
Apperyio.Entity = new Apperyio.EntityFactory({
    "Number": {
        "type": "number"
    },
    "Boolean": {
        "type": "boolean"
    },
    "String": {
        "type": "string"
    }
});
Apperyio.getModel = Apperyio.Entity.get.bind(Apperyio.Entity);

/**
 * Data storage
 */
Apperyio.storage = {

    "firstName": new $a.SessionStorage("firstName", "String"),

    "locationCity": new $a.LocalStorage("locationCity", "String"),

    "userFbId": new $a.LocalStorage("userFbId", "String"),

    "ageTemp": new $a.LocalStorage("ageTemp", "String"),

    "access_token": new $a.LocalStorage("access_token", "String"),

    "distance": new $a.SessionStorage("distance", "String"),

    "aboutMe": new $a.SessionStorage("aboutMe", "String"),

    "profileFirstName": new $a.SessionStorage("profileFirstName", "String"),

    "profileAge": new $a.SessionStorage("profileAge", "String"),

    "profileLocation": new $a.SessionStorage("profileLocation", "String"),

    "profileAboutMe": new $a.SessionStorage("profileAboutMe", "String"),

    "profilePictureUrl": new $a.SessionStorage("profilePictureUrl", "String")
};