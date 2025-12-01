import { Input } from "@/components/ui/input";
import { useUser } from "../hooks/useUser";
import { Button } from "@/components/ui/button";
import { CreditCardIcon } from "@/assets/icons/CreditCardIcon";
import { ImageIcon } from "@/assets/icons/ImageIcon";

const ProfileIndex = () => {
  const { t, handleImage, preview, fileInputRef,handleClick } = useUser();

  return (
    <div className="w-full flex flex-col items-center justify-center">
       <div
      className="relative flex items-center justify-center cursor-pointer"
      onClick={handleClick}
    >
      <div className="w-40 h-40 rounded-full border-4 border-sky-200 flex items-center justify-center bg-inherit overflow-hidden">
        <img
          src={preview}
          alt="avatar"
          className="size-full object-contain"
        />
      </div>

      <div className="absolute right-0 top-3/4 -translate-y-1/2 bg-sky-400 shadow-md rounded-full p-1">
        <ImageIcon className="w-4 h-4 stroke-gray-100" />
      </div>
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        onChange={handleImage}
        className="hidden"
      />
    </div>
      <p className="mt-4 text-3xl text-text-base font-bold">
        {t("profile-header")}
      </p>
      <p className="mt-1 mb-4 text-text-secondary text-sm font-medium">
        {t("profile-subHeader")}
      </p>
      <div className="w-11/12">
        <Input placeholder={t("profile-fullname-placeholder")} />
      </div>
      <div className="w-11/12 my-4">
        <Input
          placeholder={t("profile-phone-placeholder")}
          addonAfter={
            <div className="text-xs bg-sky-300 px-2 py-1 rounded-md cursor-pointer text-gray-100">
              {t("verify")}
            </div>
          }
        />
      </div>
      <div className="w-11/12">
        <Input
          placeholder={t("profile-email-placeholder")}
          addonAfter={
            <div className="text-xs bg-sky-300 px-2 py-1 rounded-md cursor-pointer text-gray-100">
              {t("verify")}
            </div>
          }
        />
      </div>{" "}
      <Button size="lg" className="w-2/3 mt-6">
        {t("profile-submit-btn")}
      </Button>
      <Button size="lg" className="w-1/3 mt-6">
        <CreditCardIcon />
        <span>{t("profile-cards-btn")}</span>
      </Button>
    </div>
  );
};

export default ProfileIndex;
