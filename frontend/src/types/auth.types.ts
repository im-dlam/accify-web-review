export interface ProfileType {
    id: string;
    username: string;
    balance: number;
    is_active: boolean
}

export interface LoginType {
    status: string;
    message: string;
    profile : ProfileType
}


export interface LoginRequest {
    username: string;
    password: string;
}


export interface RegisterRequest extends LoginRequest {
    email: string;
}

export interface RegisterType extends LoginType {};