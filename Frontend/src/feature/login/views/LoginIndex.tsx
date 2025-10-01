import { GoogleIcon } from "@/assets/icons/GoogleIcon";
import { UserNameIcon } from "@/assets/icons/UserNameIcon";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ContactRound } from "lucide-react";
import { Span } from "next/dist/trace";
import { useRouter } from "next/navigation";

const LoginIndex = () => {
  const router = useRouter();

  return (
    <>
      <div className="w-full">
        <div className="w-full flex flex-col justify-center items-center">
          <div className="character">
            <img src="/character.png" alt="character" className="size-40" />
          </div>
          <p className="mt-4 text-3xl text-text-base font-bold">
            Welcome, friend!
          </p>
          <p className="mt-1 mb-4 text-text-secondary text-sm font-medium">
            Welcome back, please log in to continue.
          </p>
          <div className="w-10/12">
            <Input
              placeholder="Email or Phone Number"
              addonAfter={
                <span className="bg-sky-100 dark:bg-sky-900 size-9 rounded-md p-1 flex items-center justify-center">
                  <UserNameIcon className="size-6 stroke-2 stroke-text-link"/>
                </span>
              }
              onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                console.log(e.target.value)
              }
            />
          </div>
        </div>
        <div className="w-full flex flex-col items-center justify-center mt-32">
          <Button variant="destructive" className="h-11 flex items-center mb-4">
            <GoogleIcon className="size-[18px]"/>
            <span className="text-text-base">Sign in with Google</span>
          </Button>
          <Button size="lg" onClick={() => router.push("/auth/otp")}>
            Login
          </Button>
        </div>
      </div>
    </>
  );
};

export default LoginIndex;
