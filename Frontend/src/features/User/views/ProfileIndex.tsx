import { useTranslations } from "next-intl";

const ProfileIndex = () =>{
  const t = useTranslations();

    return(
        <div className="w-full flex flex-col items-center justify-center">
        <h2>{t("profile-header")}</h2>
        </div>
    )
}

export default ProfileIndex