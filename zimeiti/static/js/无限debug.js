(function () {
    'use strict';
    var cookie_cache = document.cookie;
    Object.defineProperty(document, 'cookie', {
        get: function () {
            console.log(cookie_cache);
            return cookie_cache;
        },
        set: function (val) {
            debugger;
            var cookie = val.split(";")[0];
            var ncookie = cookie.split("=");
            var flag = false;
            var cache = cookie_cache.split(";");
            cache = cache.map(function (a) {
                if (a.split("=")[0] === ncookie[0]) {
                    flag = true;
                    return cookie;
                }
                return a;
            })
            cookie_cache = cache.join(";");
            if (!flag) {
                cookie_cache += cookie + ";";
            }
        },
    });
})();


console.error = function(){}