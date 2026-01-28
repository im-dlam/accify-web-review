import React, { useContext, createContext, useState, useEffect } from "react";
import { useCurrentUser } from "./hooks/useUser";
interface UserTypeContext {
  user: string | null;
  isLoading: boolean;
}

const UserContext = createContext<UserTypeContext | undefined>(undefined);

export const UserProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const {data, isLoading, refetch} = useCurrentUser();
  return (
    <UserContext.Provider value={{ user: data?.username || null,  isLoading}}>
      {children}
    </UserContext.Provider>
  );
};

export default function useUser(){
    const ctx = useContext(UserContext);
    if(!ctx) throw new Error("Fetch user error!");

    return ctx;
}