import { useQuery } from "@tanstack/react-query";
import * as controller from "../helpers/controller";
import { useTranslations } from "next-intl";
import { useRef, useState } from "react";
import { useForm } from "react-hook-form";
import { profileSchema, ProfileFormData } from "../interfaces/schema";
import { zodResolver } from "@hookform/resolvers/zod";

export const useUser = () => {
  const t = useTranslations();
  const fileInputRef = useRef<any>(null);

  const [preview, setPreview] = useState("/character.png");

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  const handleImage = (e: any) => {
    const file = e.target.files[0];
    if (!file) return;

    const url = URL.createObjectURL(file);
    setPreview(url);
  };

  const { data: getProfileData, isPending: getProfileDataIsPending } = useQuery(
    controller.GetProfileApiController()
  );

  const {
    watch,
    setValue,
    handleSubmit,
    getValues,
    formState: { errors },
  } = useForm<ProfileFormData>({
    resolver: zodResolver(profileSchema),
    mode: "onBlur",
    values:{
      name:getProfileData?.name?? '',
      email:getProfileData?.email ?? '',
      phone_number:getProfileData?.phone_number ?? ''
    }
  });


  return {
    t,
    preview,
    handleImage,
    handleClick,
    fileInputRef,
    getProfileData,
    getProfileDataIsPending,
    watch,
    setValue,
    handleSubmit,
    errors,
    getValues,
  };
};
