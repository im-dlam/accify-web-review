import type {UserRead} from '../types'

export const getCurrentUser = async(): Promise<UserRead> => {
    const resp = await fetch('http://localhost:8000/api/users/me', {
        method: 'GET',
        headers: {'Content-Type': 'application/json' },
        credentials: "include"

    })
    if(!resp.ok) throw Error("Get User failed")
    return resp.json()
}