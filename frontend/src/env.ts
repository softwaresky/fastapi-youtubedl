const env = process.env.VUE_APP_ENV;

let envApiUrl = '';

if (env === 'production') {
    envApiUrl = process.env.VUE_APP_DOMAIN_PROD == undefined ? `https://${process.env.VUE_APP_DOMAIN_PROD}` : '';
} else if (env === 'staging') {
    envApiUrl = process.env.VUE_APP_DOMAIN_STAG == undefined ? `https://${process.env.VUE_APP_DOMAIN_STAG}` : '';
} else if (env === 'development') {
    envApiUrl = process.env.VUE_APP_DOMAIN_DEV == undefined ? `http://${process.env.VUE_APP_DOMAIN_DEV}` : '';
} else if (env === 'local') {
    envApiUrl = '';
} else {
    envApiUrl = process.env.VUE_APP_DOMAIN == undefined ? `http://${process.env.VUE_APP_DOMAIN}` : '';
}

export const apiUrl = envApiUrl;
export const appName = process.env.VUE_APP_NAME;
