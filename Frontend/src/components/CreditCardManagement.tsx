"use client";

import React, { useState } from "react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Plus, Trash2, CreditCard } from "lucide-react";

interface CreditCard {
  id: string;
  name: string;
  number: string;
  bank?: string;
  logo?: string;
}

interface BankInfo {
  name: string;
  logo: string;
  pattern: RegExp;
}

const banks: BankInfo[] = [
  { name: "بانک ملی", logo: "🏦", pattern: /^603799|^589210|^627353/ },
  { name: "بانک سپه", logo: "🏛️", pattern: /^589210|^627353/ },
  { name: "بانک ملت", logo: "💳", pattern: /^610433|^991975/ },
  { name: "بانک تجارت", logo: "🏪", pattern: /^627353|^585983/ },
  { name: "بانک صادرات", logo: "🚢", pattern: /^603769|^903769/ },
  { name: "بانک پارسیان", logo: "🌟", pattern: /^622106|^627884/ },
  { name: "بانک پاسارگاد", logo: "🦁", pattern: /^502229|^639347/ },
  { name: "بانک سامان", logo: "⚡", pattern: /^621986/ },
  { name: "بانک شهر", logo: "🏙️", pattern: /^502806|^504706/ },
  { name: "بانک آینده", logo: "🔮", pattern: /^636214/ },
];

const formatCardNumber = (value: string): string => {
  // Remove all non-digits
  const digits = value.replace(/\D/g, "");

  // Limit to 16 digits
  const limitedDigits = digits.slice(0, 16);

  // Add spaces every 4 digits
  return limitedDigits.replace(/(\d{4})(?=\d)/g, "$1 ");
};

const detectBank = (cardNumber: string): BankInfo | null => {
  const digits = cardNumber.replace(/\s/g, "");

  // Need at least 6 digits to detect bank
  if (digits.length < 6) return null;

  // Check first 6 digits
  const prefix = digits.slice(0, 6);

  for (const bank of banks) {
    if (bank.pattern.test(prefix)) {
      return bank;
    }
  }

  return null;
};

export const CreditCardManagement: React.FC = () => {
  const [cards, setCards] = useState<CreditCard[]>([
    {
      id: "1",
      name: "علی رضایی",
      number: "6037 9912 3456 7890",
      bank: "بانک ملی",
      logo: "🏦",
    },
  ]);

  const [isAddingCard, setIsAddingCard] = useState(false);
  const [newCardName, setNewCardName] = useState("");
  const [newCardNumber, setNewCardNumber] = useState("");
  const [detectedBank, setDetectedBank] = useState<BankInfo | null>(null);

  const handleCardNumberChange = (value: string) => {
    const formatted = formatCardNumber(value);
    setNewCardNumber(formatted);

    // Detect bank based on current input
    const bank = detectBank(formatted);
    setDetectedBank(bank);
  };

  const addCard = () => {
    if (!newCardName.trim() || newCardNumber.replace(/\s/g, "").length !== 16) {
      return;
    }

    const newCard: CreditCard = {
      id: Date.now().toString(),
      name: newCardName.trim(),
      number: newCardNumber,
      bank: detectedBank?.name,
      logo: detectedBank?.logo,
    };

    setCards([...cards, newCard]);
    setNewCardName("");
    setNewCardNumber("");
    setDetectedBank(null);
    setIsAddingCard(false);
  };

  const deleteCard = (id: string) => {
    setCards(cards.filter((card) => card.id !== id));
  };

  return (
    <div className="w-full max-w-md mx-auto p-4 space-y-4">
      {/* Header with Add Button */}
      <div className="flex justify-between items-center">
        <h3 className="text-lg font-semibold text-text-base">کارت های شما</h3>
        <Button
          onClick={() => setIsAddingCard(!isAddingCard)}
          size="sm"
          className="bg-blue-500 hover:bg-blue-600 text-white"
        >
          <Plus className="w-4 h-4 mr-2" />
          افزودن کارت
        </Button>
      </div>

      {/* Add New Card Form */}
      {isAddingCard && (
        <div className="bg-input rounded-lg p-4 space-y-3 border border-text-secondary/20">
          <div>
            <label className="block text-sm font-medium text-text-base mb-1">
              نام صاحب کارت
            </label>
            <Input
              value={newCardName}
              onChange={(e) => setNewCardName(e.target.value)}
              placeholder="مثال: علی رضایی"
              className="bg-back border-text-secondary/30"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-text-base mb-1">
              شماره کارت (16 رقم)
            </label>
            <Input
              dir="ltr"
              value={newCardNumber}
              onChange={(e) => handleCardNumberChange(e.target.value)}
              placeholder="0000 0000 0000 0000"
              className="bg-back text-left border-text-secondary/30 font-mono"
              maxLength={19} // 16 digits + 3 spaces
            />
          </div>

          {/* Bank Detection Display */}
          {detectedBank && (
            <div className="flex items-center space-x-2 p-2 bg-blue-50 dark:bg-blue-900/20 rounded-md">
              <span className="text-2xl">{detectedBank.logo}</span>
              <span className="text-sm text-text-base">{detectedBank.name}</span>
            </div>
          )}

          <div className="flex space-x-2">
            <Button
              onClick={addCard}
              disabled={!newCardName.trim() || newCardNumber.replace(/\s/g, "").length !== 16}
              className="flex-1 bg-green-500 hover:bg-green-600 text-white"
            >
              ذخیره کارت
            </Button>
            <Button
              onClick={() => {
                setIsAddingCard(false);
                setNewCardName("");
                setNewCardNumber("");
                setDetectedBank(null);
              }}
              variant="outline"
              className="flex-1"
            >
              انصراف
            </Button>
          </div>
        </div>
      )}

      {/* Cards List */}
      <div className="space-y-3">
        {cards.length === 0 ? (
          <div className="text-center py-8 text-text-secondary">
            <CreditCard className="w-12 h-12 mx-auto mb-2 opacity-50" />
            <p>هیچ کارتی اضافه نشده</p>
          </div>
        ) : (
          cards.map((card) => (
            <div
              key={card.id}
              className="bg-gradient-to-br from-sky-500 via-sky-600 to-sky-700 rounded-2xl p-6 text-white shadow-2xl relative overflow-hidden transform hover:scale-105 transition-all duration-300 ease-in-out border border-sky-400/30"
            >
              {/* Animated Background Pattern */}
              <div className="absolute inset-0 opacity-5">
                <div className="absolute top-6 right-6 w-12 h-12 border-2 border-white rounded-full animate-pulse"></div>
                <div className="absolute top-10 right-10 w-6 h-6 border border-white rounded-full"></div>
                <div className="absolute bottom-6 left-6 w-8 h-8 border border-white rotate-45"></div>
                <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-20 h-20 border border-white/20 rounded-full"></div>
              </div>

              {/* Shimmer Effect */}
              <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent transform -skew-x-12 animate-pulse"></div>

              {/* Card Content */}
              <div className="relative z-10">
                <div className="flex justify-between items-start mb-6">
                  <div className="flex items-center space-x-3">
                    {card.logo && <span className="text-2xl drop-shadow-lg">{card.logo}</span>}
                    {card.bank && <span className="text-sm font-medium opacity-90 tracking-wide">{card.bank}</span>}
                  </div>
                  <Button
                    onClick={() => deleteCard(card.id)}
                    size="sm"
                    variant="ghost"
                    className="text-white/80 hover:text-white hover:bg-white/10 p-2 h-9 w-9 rounded-full backdrop-blur-sm transition-all duration-200"
                  >
                    <Trash2 className="w-4 h-4" />
                  </Button>
                </div>

                {/* Card Chip */}
                <div className="flex items-center mb-4">
                  <div className="w-10 h-8 bg-gradient-to-br from-yellow-400 to-yellow-600 rounded-md shadow-inner flex items-center justify-center">
                    <div className="w-6 h-4 bg-gradient-to-br from-gray-300 to-gray-500 rounded-sm border border-gray-400"></div>
                  </div>
                  <div className="ml-3 text-xs text-white/60 font-medium tracking-wider">CHIP</div>
                </div>

                {/* Card Number */}
                <div className="mb-6">
                  <p className="text-xl text-center font-mono tracking-[0.2em] font-bold drop-shadow-sm" dir="ltr">
                    {card.number}
                  </p>
                </div>

                {/* Card Details */}
                <div className="flex justify-between items-end">
                  <div className="flex flex-col">
                    <span className="text-xs text-white/60 uppercase tracking-wider mb-1">Card Holder</span>
                    <span className="text-base font-semibold tracking-wide">{card.name}</span>
                  </div>
                  <div className="flex flex-col items-end">
                    <span className="text-xs text-white/60 uppercase tracking-wider mb-1">Valid Thru</span>
                    <span className="text-base font-mono font-semibold">12/28</span>
                  </div>
                </div>

                {/* Card Brand Logo */}
                <div className="absolute bottom-4 right-4 opacity-80">
                  <div className="w-12 h-8 bg-gradient-to-r from-blue-600 to-blue-800 rounded flex items-center justify-center">
                    <span className="text-white text-xs font-bold tracking-wider">VISA</span>
                  </div>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
