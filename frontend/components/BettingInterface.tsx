'use client';

import { useState } from 'react';
import { usePrivy } from '@privy-io/react-auth';
import { Finalist } from '@/types';

interface BettingInterfaceProps {
  finalist: Finalist;
  onPlaceBet: (finalistId: string, amount: number) => Promise<void>;
}

export default function BettingInterface({ finalist, onPlaceBet }: BettingInterfaceProps) {
  const { login, logout, authenticated, user } = usePrivy();
  const [betAmount, setBetAmount] = useState<number>(0.1);
  const [isPlacingBet, setIsPlacingBet] = useState(false);
  const [betPlaced, setBetPlaced] = useState(false);

  const betOptions = [0.1, 0.5, 1.0, 2.5, 5.0];

  const handlePlaceBet = async () => {
    if (!authenticated) {
      await login();
      return;
    }

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

  const getUserDisplay = () => {
    if (user?.email?.address) return user.email.address;
    if (user?.wallet?.address) {
      return user.wallet.address.slice(0, 6) + '...' + user.wallet.address.slice(-4);
    }
    if (user?.google?.email) return user.google.email;
    return 'User';
  };

  // Not authenticated - show login prompt
  if (!authenticated) {
    return (
      <div className="bg-white border-2 border-black p-4">
        <div className="border-b-2 border-black bg-black px-3 py-1.5 -mx-4 -mt-4 mb-4">
          <h3 className="text-xs font-bold uppercase tracking-wider text-white">
            Place Bet (SOL)
          </h3>
        </div>

        <div className="mb-3 text-xs uppercase text-black opacity-60 text-center">
          Login to place bets
        </div>

        <button
          onClick={login}
          className="w-full py-3 px-4 bg-black text-white border-2 border-black hover:bg-gray-900 hover:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:-translate-y-0.5 font-bold text-xs uppercase tracking-wide transition-all"
        >
          Login with Wallet / Email / Google
        </button>

        <div className="mt-3 text-xs text-black opacity-60 text-center font-mono">
          Supports Phantom, Solflare, or create embedded wallet
        </div>
      </div>
    );
  }

  // Authenticated - show betting interface
  return (
    <div className="bg-white border-2 border-black p-3">
      <div className="border-b-2 border-black bg-black px-3 py-1.5 -mx-3 -mt-3 mb-3">
        <h3 className="text-xs font-bold uppercase tracking-wider text-white">
          Place Bet (SOL)
        </h3>
      </div>

      {/* User Info */}
      <div className="mb-3 bg-gray-50 border border-black p-2 flex justify-between items-center">
        <div className="text-xs font-mono">
          <span className="opacity-60">LOGGED IN AS:</span>{' '}
          <span className="font-bold">{getUserDisplay()}</span>
        </div>
        <button
          onClick={logout}
          className="text-xs underline opacity-60 hover:opacity-100"
        >
          Logout
        </button>
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
            PLACING BET...
          </span>
        ) : betPlaced ? (
          '✓ BET PLACED!'
        ) : (
          'PLACE BET'
        )}
      </button>

      {/* Note */}
      <div className="mt-3 text-xs text-black opacity-60 text-center font-mono">
        {user?.wallet?.address ? 'Using connected wallet' : 'Using embedded wallet'}
      </div>
    </div>
  );
}
