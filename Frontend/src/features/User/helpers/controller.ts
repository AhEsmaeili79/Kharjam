import { queryOptions, useMutation } from '@tanstack/react-query';
import * as api from './api';

export const GetProfileApiController = (
) => queryOptions({
  queryKey: ['getProfileApi'],
  queryFn: async () => {
    const res = await api.getProfileApi;
    return res;
  },
});

export const UpdateProfileApiController = () =>
  useMutation({
    mutationFn: api.updateProfileApi,
  });

