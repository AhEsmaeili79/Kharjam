import { queryOptions, useMutation } from "@tanstack/react-query";
import * as api from "./api";
const { getProfileApi, updateProfileApi } = api.getUserService();

export const GetProfileApiController = (
  reset: any,
  setProfileData:Function
) =>
  queryOptions({
    queryKey: ["getProfileApi"],
    queryFn:async () =>{
     return getProfileApi().then((res: any) => {
      setProfileData(res.data)
      reset({
        name:res.data.name,
        email:res.data.email,
        phone_number: res.data.phone_number
      })
        return res.data;
      })}
      
  });

export const UpdateProfileApiController = () =>
  useMutation({
    mutationFn: updateProfileApi,
  });
