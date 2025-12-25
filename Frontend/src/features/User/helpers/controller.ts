import { queryOptions, useMutation, useQueryClient } from "@tanstack/react-query";
import * as api from "./api";
import { UserUpdate } from "./api.schemas";
import { notify } from "@/components/ui/sonner";
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

  export const UpdateProfileApiController = (
    body: UserUpdate
 ) => {
    const queryClient = useQueryClient();
    return {
       mutationKey: ["updateProfileDataApi"],
       mutationFn: () => updateProfileApi(body),
       onSuccess: (res: any) => {
          notify.success(res.data.message);
          queryClient.invalidateQueries({
             queryKey: ["getProfileDataApi"]
          });
       },
       onError: (error: any) => {
        notify.error(error.message);
       }
    };
 };
