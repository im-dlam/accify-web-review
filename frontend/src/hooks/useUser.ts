import { useQuery } from "@tanstack/react-query";
import type {UserRead} from "../types"
import {getCurrentUser} from "../services/user"



export const useCurrentUser = () => useQuery({
    queryKey:["currentUser"],
    queryFn: getCurrentUser,
    staleTime: 1000 * 60 * 10,
    refetchOnWindowFocus: false,
    retry: 1
})