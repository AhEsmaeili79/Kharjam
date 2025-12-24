import { queryOptions, useMutation } from "@tanstack/react-query";
import * as api from "./api";
const { getProfileApi, updateProfileApi } = api.getUserService();

export const GetProfileApiController = () =>
  queryOptions({
    queryKey: ["getProfileDataApi"],
    queryFn: async () => {
      return getProfileApi().then((res: any) => {
        return res.data;
      });
    },
  });

export const UpdateProfileApiController = () =>
  useMutation({
    mutationFn: updateProfileApi,
  });
