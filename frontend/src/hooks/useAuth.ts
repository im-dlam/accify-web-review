import { useMutation } from "@tanstack/react-query";
import type { LoginType, LoginRequest, RegisterRequest, ProfileType } from "../types";
import {loginUser, logoutUser, registerUser} from '../services/auth'
import { queryClient } from "../App"

export const useLogin = () => useMutation({
    mutationKey: ["login"],
    mutationFn: ({ username, password }: LoginRequest): Promise<LoginType> => loginUser(username, password),
    onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['currentUser'] });
        }
    })

export const useRegister = () => useMutation({
    mutationKey: ["register"],
    mutationFn: ({email, username, password}: RegisterRequest): Promise<ProfileType> => registerUser(email, username, password),
    onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['currentUser'] });
    }
})

export const useLogout = () => useMutation({
    mutationKey: ["logout"],
    mutationFn: () => logoutUser(),
    onSuccess: () => {
        queryClient.clear()
    }
})
