import { use } from 'react';
import type {LoginType, RegisterType, ProfileType} from '../types';


export const loginUser =  async(username: string, password: string): Promise<LoginType> => {
    try {
        const resp = await fetch('http://localhost:8000/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                username: username,
                password: password
            }),
            credentials: "include"
        })

        if(!resp.ok) throw new Error("login failed")

        return resp.json()
    } catch(e) {
        console.error("Login error:", e);
        throw e;
    }
}

export const registerUser = async(email: string, username: string, password: string): Promise<ProfileType> => {
    try {
        const resp = await fetch('http://localhost:8000/api/users/signup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                email: email,
                username: username,
                password: password
            }),
            credentials: "include"
        })

        if(!resp.ok) throw new Error("Register failed");
        return resp.json();
    }
    catch(e) {
        console.error("Login error:", e);
        throw e;
    }
}

export const logoutUser = async() => {
    const resp = await fetch('http://localhost:8000/api/users/logout', {
        method: 'POST',
        headers: {'Content-Type': 'application/json' },
        credentials: "include"
    })

    if(!resp.ok) throw Error("logout failed")
    return resp.json()
    }

