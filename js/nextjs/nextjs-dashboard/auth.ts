import NextAuth from "next-auth"
import CredintialsProvider from "next-auth/providers/credentials"
import type { NextAuthConfig } from "next-auth"

export const config = {
    providers: [
        CredintialsProvider({
            name: 'Credentials',
            credentials: {
                username: { label: "Username", type: "text" },
                password: { label: "Password", type: "password" }
            },
            async authorize(credentials, request) {
                const user = { id: "1", name: 'J Smith', email: 'j_smith@example.com' }
                if (credentials.username === 'j_smith' && credentials.password === 'password') {
                    return user
                }
                return null
            }
        }),
    ]
} satisfies NextAuthConfig

export const { handlers: {GET, POST}, auth, signIn, signOut } = NextAuth(config)