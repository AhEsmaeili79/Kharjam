// "use client";

// import { ReactNode } from "react";
// import { NextIntlClientProvider } from "next-intl";
// import { defaultLocale } from "@/i18n";
// import "../globals.css";
// import { useLocale } from "@/utils/useLocaleUtil";
// import ToggleThemeComponent from "@/components/ToggleThemeComponent";
// import ChangeLocaleComponent from "@/components/ChangeLocaleComponent";

// export default function RootLayout({ children }: { children: ReactNode }) {
//   const { currentLocale, messages } = useLocale();

//   return (
//     <html lang={defaultLocale} dir={defaultLocale === "fa" ? "rtl" : "ltr"}>
//       <body>
//         <NextIntlClientProvider locale={currentLocale} messages={messages}>
//           <div className="auth-layout">
//          <div className="absolute top-5 right-5">
//           <ToggleThemeComponent/>
//          </div>
//          <div className="absolute top-5 left-5">
//             <ChangeLocaleComponent/>
//          </div>
//             {children}
//           </div>
//         </NextIntlClientProvider>
//       </body>
//     </html>
//   );
// }


"use client";

import { ReactNode } from "react";
import { NextIntlClientProvider } from "next-intl";
import { useLocale } from "@/utils/useLocaleUtil";
import ToggleThemeComponent from "@/components/ToggleThemeComponent";
import ChangeLocaleComponent from "@/components/ChangeLocaleComponent";
import "../globals.css";

export default function AuthLayout({ children }: { children: ReactNode }) {
  const { currentLocale, messages } = useLocale();

  return (
    <NextIntlClientProvider locale={currentLocale} messages={messages}>
      <div className="auth-layout" suppressHydrationWarning>
        <div className="absolute top-5 right-5">
          <ToggleThemeComponent />
        </div>
        <div className="absolute top-5 left-5">
          <ChangeLocaleComponent />
        </div>
        {children}
      </div>
    </NextIntlClientProvider>
  );
}


