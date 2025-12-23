import { useQuery } from "@tanstack/react-query";
import * as controller from "../helpers/controller";
import { useTranslations } from "next-intl";
import { useRef, useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import { profileSchema, ProfileFormData } from "../interfaces/schema";
import { zodResolver } from "@hookform/resolvers/zod";

export const useUser = () => {
  const t = useTranslations();
  const fileInputRef = useRef<any>(null);
  const [preview, setPreview] = useState("/character.png");
  const [profileData, setProfileData] = useState({
    email: "",
    name: "",
    phone_number: "",
  });

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  const handleImage = (e: any) => {
    const file = e.target.files[0];
    if (!file) return;

    const url = URL.createObjectURL(file);
    setPreview(url);
  };

  const {
    watch,
    setValue,
    reset,
    handleSubmit,
    register,
    getValues,
    formState: { errors },
  } = useForm<ProfileFormData>({
    resolver: zodResolver(profileSchema),
    mode: "onBlur",
    defaultValues:{
      name: profileData.name,
      email: profileData.email,
      phone_number: profileData.phone_number
    }
  });

  const { data: getProfileData, isPending: getProfileDataIsPending } = useQuery(
    controller.GetProfileApiController(reset, setProfileData)
  );

  console.log(watch("email"), "watch"),
  console.log(getValues("email"), "getval");

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
    register,
    getValues,
  };
};
