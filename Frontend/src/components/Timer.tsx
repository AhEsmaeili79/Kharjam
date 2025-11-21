"use client";
import { useEffect, useState, useRef } from "react";

interface TimerProps {
  minutes: number;
  storageKey?: string;
}

export default function Timer({
  minutes,
  storageKey = "timerRemaining",
}: TimerProps) {
  const totalSeconds = minutes * 60;

  const [timeLeft, setTimeLeft] = useState<number | null>(null);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  const startTimer = (initialValue: number) => {
    setTimeLeft(initialValue);
    localStorage.setItem(storageKey, initialValue.toString());

    if (intervalRef.current) clearInterval(intervalRef.current);

    intervalRef.current = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev === null) return prev;

        const newValue = prev - 1;

        if (newValue <= 0) {
          clearInterval(intervalRef.current!);
          localStorage.removeItem(storageKey);
          return 0;
        }

        localStorage.setItem(storageKey, newValue.toString());
        return newValue;
      });
    }, 1000);
  };
  useEffect(() => {
    const saved = localStorage.getItem(storageKey);

    if (saved) {
      const savedValue = parseInt(saved);
      if (savedValue > 0) {
        startTimer(savedValue);
        return;
      }
    }
    startTimer(totalSeconds);
  }, []);

  useEffect(() => {
    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, []);

  if (timeLeft === null) return null;

  const minutesDisplay = Math.floor(timeLeft / 60);
  const secondsDisplay = (timeLeft % 60).toString().padStart(2, "0");

  return (
    <div className="text-text-secondary transition-all duration-500 animate-[fadeScale_0.4s_ease]">
      {minutesDisplay}:{secondsDisplay}
    </div>
  );
}
