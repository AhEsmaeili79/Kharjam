import { z } from "zod";

export const profileSchema = z.object({
  name: z.string().min(2, { message: "Name must be at least 2 characters" }).max(100, { message: "Name must be less than 100 characters" }),
  phone_number: z.string().regex(/^(\+98|0)?9\d{9}$/, { message: "Please enter a valid Iranian phone number" }),
  email: z.string().email({ message: "Please enter a valid email address" }).optional().or(z.literal("")),
});

export type ProfileFormData = z.infer<typeof profileSchema>;