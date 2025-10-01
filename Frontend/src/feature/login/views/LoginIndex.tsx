import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
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
                <span className="flex items-center justify-center text-text-base size-6 rounded-full bg-sky-500">0</span>
              }
              onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                console.log(e.target.value)
              }
            />
          </div>
        </div>
        <div className="w-full flex flex-col items-center justify-center mt-32">
          <Button variant="destructive" className="h-11 flex items-center mb-4">
            <img src="/google-icon.svg" alt="Google" className="w-6 h-6" />
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
