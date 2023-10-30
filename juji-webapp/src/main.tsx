import React, {useContext} from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'
import {AuthContext, AuthProvider, IAuthContext, TAuthConfig, TRefreshTokenExpiredEvent} from "react-oauth2-code-pkce"

const authConfig: TAuthConfig = {
    clientId: 'lmdm',
    authorizationEndpoint: 'http://localhost:8000/auth',
    tokenEndpoint: 'http://localhost:8000/token',
    redirectUri: 'http://localhost:5173/',
    scope: 'someScope openid',
    onRefreshTokenExpire: (event: TRefreshTokenExpiredEvent) => window.confirm('Session expired. Refresh page to continue using the site?') && event.login(),
}

const UserInfo = (): JSX.Element => {
    const {token, tokenData} = useContext<IAuthContext>(AuthContext)

    return <>
        <h4>Access Token</h4>
        <pre>{token}</pre>
        <h4>User Information from JWT</h4>
        <pre>{JSON.stringify(tokenData, null, 2)}</pre>
    </>
}


ReactDOM.createRoot(document.getElementById('root')!).render(
    <React.StrictMode>
        <AuthProvider authConfig={authConfig}>
            <UserInfo/>
        </AuthProvider>
    </React.StrictMode>,
)
