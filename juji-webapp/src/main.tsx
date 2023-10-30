import React from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'

import App from "./App.tsx";
import {AuthProvider, TAuthConfig, TRefreshTokenExpiredEvent} from "react-oauth2-code-pkce";

const authConfig: TAuthConfig = {
    clientId: 'lmdm',
    authorizationEndpoint: 'http://localhost:8000/oidc/auth',
    tokenEndpoint: 'http://localhost:8000/oidc/token',
    redirectUri: 'http://localhost:5173/',
    scope: 'openid userinfo',
    onRefreshTokenExpire: (event: TRefreshTokenExpiredEvent) => window.confirm('Session expired. Refresh page to continue using the site?') && event.login(),
}

ReactDOM.createRoot(document.getElementById('root')!).render(
    <React.StrictMode>
        <AuthProvider authConfig={authConfig}>
            <App/>
        </AuthProvider>
    </React.StrictMode>,
)
