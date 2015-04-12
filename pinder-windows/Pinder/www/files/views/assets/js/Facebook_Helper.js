(function(context) {
    Helper = {};
    var ref;
    // var projectId = window.location.href.split("/")[5];
    
    Helper.init = function() {
        
        var callbackUrl = "http://appery.io/app/view/" + Facebook_Settings.project_id + "/dashboard.html";
        var url = "https://www.facebook.com/dialog/oauth?client_id=" + Facebook_Settings['client_id'] + "&redirect_uri=" + callbackUrl + "&scope=&response_type=token";
        
        if (this.isPhoneGapApp()) {
            ref = window.open(url, '_blank', 'location=yes');
            ref.addEventListener("loadstart", this.getAccessToken);
        } else {
            window.open(url, "_self");
            
        }
    };
    
    Helper.getAccessToken = function(event) {
        
        if (event.url.indexOf('access_token') >= 0) {
            console.log("Extracting access_token...");
            var params = event.url.split("access_token=");
            var _access_token = params[1].slice(0, params[1].indexOf("&"));
            localStorage.setItem('access_token', _access_token);
            ref.close();
            Appery.navigateTo('dashboard', {});
            
        }
        
    };
    
    Helper.isPhoneGapApp = function() {
        return (document.URL.indexOf('http://') === -1 && document.URL.indexOf('https://') === -1);
    };
    
    if (window.location.href.indexOf("access_token") != -1) {
        var hashFromFb = window.location.hash;
        window.location.hash = '';
        var paramsFromFb = hashFromFb.substring(1).split("&");
        var access_token = paramsFromFb[0].split("=")[1];
        localStorage.setItem('access_token', access_token);
        
    }
    
    context.Helper = Helper;
})(window);