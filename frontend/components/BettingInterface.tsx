'use client';

import { useState } from 'react';
import { Finalist } from '@/types';

interface BettingInterfaceProps {
  finalist: Finalist;
  onPlaceBet: (finalistId: string, amount: number) => Promise<void>;
}

export default function BettingInterface({ finalist, onPlaceBet }: BettingInterfaceProps) {
  const [betAmount, setBetAmount] = useState<number>(0.1);
  const [isPlacingBet, setIsPlacingBet] = useState(false);
  const [betPlaced, setBetPlaced] = useState(false);

  const betOptions = [0.1, 0.5, 1.0, 2.5, 5.0];

  const handlePlaceBet = async () => {
    setIsPlacingBet(true);
    try {
      await onPlaceBet(finalist.story.story_id, betAmount);
      setBetPlaced(true);
      setTimeout(() => setBetPlaced(false), 3000);
    } catch (error) {
      console.error('Bet placement failed:', error);
    } finally {
      setIsPlacingBet(false);
    }
  };

  return (
    <div className="bg-white border-2 border-black p-3">
      <div className="border-b-2 border-black bg-black px-3 py-1.5 -mx-3 -mt-3 mb-3">
        <h3 className="text-xs font-bold uppercase tracking-wider text-white">
          Place Bet (SOL)
        </h3>
      </div>

      {/* Bet Amount Selection */}
      <div className="mb-3">
        <div className="text-xs uppercase text-black opacity-60 mb-2">
          Select Amount
        </div>
        <div className="grid grid-cols-5 gap-1">
          {betOptions.map((amount) => (
            <button
              key={amount}
              onClick={() => setBetAmount(amount)}
              className={`py-2 px-1 border-2 border-black text-xs font-mono font-bold transition-all hover:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:-translate-y-0.5 ${
                betAmount === amount
                  ? 'bg-black text-white'
                  : 'bg-white text-black hover:bg-gray-50'
              }`}
              disabled={isPlacingBet}
            >
              {amount}
            </button>
          ))}
        </div>
      </div>

      {/* Custom Amount */}
      <div className="mb-3">
        <div className="text-xs uppercase text-black opacity-60 mb-2">
          Custom Amount
        </div>
        <input
          type="number"
          min="0.01"
          step="0.01"
          value={betAmount}
          onChange={(e) => setBetAmount(parseFloat(e.target.value) || 0)}
          className="w-full p-2 border-2 border-black font-mono text-sm text-black"
          disabled={isPlacingBet}
        />
      </div>

      {/* Potential Payout Info */}
      <div className="mb-3 bg-gray-50 border-2 border-black p-2">
        <div className="flex justify-between text-xs font-mono mb-1">
          <span className="text-black opacity-60">YOUR BET:</span>
          <span className="text-black font-bold">{betAmount.toFixed(2)} SOL</span>
        </div>
        <div className="flex justify-between text-xs font-mono">
          <span className="text-black opacity-60">POTENTIAL WIN:</span>
          <span className="text-black font-bold">{(betAmount * 3).toFixed(2)} SOL</span>
        </div>
        <div className="mt-2 text-xs text-black opacity-60">
          3x payout if this story wins! Pool distributed among winners.
        </div>
      </div>

      {/* Place Bet Button */}
      <button
        onClick={handlePlaceBet}
        disabled={isPlacingBet || betAmount <= 0 || betPlaced}
        className={`w-full py-3 px-4 border-2 border-black font-bold text-xs uppercase tracking-wide transition-all ${
          betPlaced
            ? 'bg-green-500 text-white border-green-700'
            : 'bg-black text-white hover:bg-gray-900 hover:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:-translate-y-0.5 disabled:opacity-50 disabled:cursor-not-allowed'
        }`}
      >
        {isPlacingBet ? (
          <span className="flex items-center justify-center gap-2">
            <span className="inline-block animate-spin rounded-full h-3 w-3 border-2 border-white border-t-transparent"></span>
            CONNECTING WALLET...
          </span>
        ) : betPlaced ? (
          '✓ BET PLACED!'
        ) : (
          'PLACE BET'
        )}
      </button>

      {/* Wallet Connection Notice */}
      <div className="mt-3 text-xs text-black opacity-60 text-center font-mono">
        Connect Phantom or Solflare wallet to place bet
      </div>
    </div>
  );
}
