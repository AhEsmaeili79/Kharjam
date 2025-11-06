import { GoogleIcon } from "@/assets/icons/GoogleIcon";
import { UserNameIcon } from "@/assets/icons/UserNameIcon";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useTranslations } from "next-intl";
import { useAuth } from "../hooks/useAuth";

const LoginIndex = () => {
  const {t, identifier, setIdentifier, requestOtpMutate, requestOtpPending } = useAuth();

  return (
    <>
      <div className="w-full">
        <div className="w-full flex flex-col justify-center items-center">
          <div className="character">
            <img src="/character.png" alt="character" className="size-40" />
          </div>
          <p className="mt-4 text-3xl text-text-base font-bold">
            {t("login-welcome")}
          </p>
          <p className="mt-1 mb-4 text-text-secondary text-sm font-medium">
            {t("login-subtext")}
          </p>
          <div className="w-10/12">
            <Input
              placeholder={t("login-input-placeholder")}
              addonAfter={
                <span className="bg-sky-100 dark:bg-sky-900 size-9 rounded-md p-1 flex items-center justify-center">
                  <UserNameIcon className="size-6 stroke-2 stroke-text-link" />
                </span>
              }
              onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                setIdentifier(e.target.value)
              }
            />
          </div>
        </div>
        <div className="w-full flex flex-col items-center justify-center mt-32">
          <Button variant="destructive" className="h-11 flex items-center mb-4">
            <GoogleIcon className="size-[18px]" />
            <span className="text-text-base">{t("login-google")}</span>
          </Button>
          <Button
            disabled={identifier === "" || requestOtpPending }
            size="lg"
            onClick={() => {
              requestOtpMutate();
            }}
          >
            {t("login-btn")}
          </Button>
        </div>
      </div>
    </>
  );
};

export default LoginIndex;
