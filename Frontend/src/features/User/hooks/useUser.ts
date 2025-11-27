// import * as controller from "../helpers/controller";
// import * as api from "../helpers/api";
import { useTranslations } from "next-intl";
import { useState } from "react";


 export const useUser = () => {
  const t = useTranslations();
  const [preview, setPreview] = useState("/character.png");

  const handleImage = (e:any) => {
    const file = e.target.files[0];
    if (!file) return;

    const url = URL.createObjectURL(file);
    setPreview(url);
  }

  return { t,preview, handleImage };
};

