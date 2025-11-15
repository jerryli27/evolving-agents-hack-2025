# x402 Wallet Integration Guide

Complete guide for integrating Solana wallet betting functionality using the x402 payment protocol.

## Overview

The Short Drama IP Factory includes a betting system where readers can bet SOL tokens on which finalist story will perform best for short drama production. The betting system uses:

- **x402 Protocol**: HTTP-native payment standard for micropayments
- **Solana Blockchain**: Fast, low-cost transactions
- **Phantom/Solflare Wallets**: Popular Solana wallet providers

## Current Status

✅ **Implemented**:
- BettingInterface component with UI
- Betting flow in FinalistsSection
- Mock betting functionality for demo

🔨 **To Implement**:
- Solana wallet adapter integration
- x402 payment protocol setup
- Backend bet tracking and payout distribution

---

## Installation

### 1. Install Required Packages

```bash
cd frontend

# Core Solana wallet adapter
npm install @solana/wallet-adapter-react \
            @solana/wallet-adapter-react-ui \
            @solana/wallet-adapter-wallets \
            @solana/web3.js

# Specific wallet adapters
npm install @solana/wallet-adapter-phantom \
            @solana/wallet-adapter-solflare

# x402 Solana React integration
npm install @payai/x402-solana-react

# OR use x402-solana for more control
npm install x402-solana
```

### 2. Backend Dependencies

```bash
cd backend

# x402 server-side verification
pip install solana
pip install anchorpy
```

---

## Frontend Implementation

### Step 1: Create Wallet Provider

Create `frontend/components/WalletProvider.tsx`:

```tsx
'use client';

import { useMemo } from 'react';
import {
  ConnectionProvider,
  WalletProvider,
} from '@solana/wallet-adapter-react';
import { WalletAdapterNetwork } from '@solana/wallet-adapter-base';
import { PhantomWalletAdapter, SolflareWalletAdapter } from '@solana/wallet-adapter-wallets';
import { WalletModalProvider } from '@solana/wallet-adapter-react-ui';
import { clusterApiUrl } from '@solana/web3.js';

// Import wallet adapter CSS
import '@solana/wallet-adapter-react-ui/styles.css';

export default function AppWalletProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  // Use devnet for testing, mainnet-beta for production
  const network = WalletAdapterNetwork.Devnet;
  const endpoint = useMemo(() => clusterApiUrl(network), [network]);

  // Configure wallets
  const wallets = useMemo(
    () => [
      new PhantomWalletAdapter(),
      new SolflareWalletAdapter(),
    ],
    []
  );

  return (
    <ConnectionProvider endpoint={endpoint}>
      <WalletProvider wallets={wallets} autoConnect>
        <WalletModalProvider>{children}</WalletModalProvider>
      </WalletProvider>
    </ConnectionProvider>
  );
}
```

### Step 2: Wrap App with Wallet Provider

Update `frontend/app/layout.tsx`:

```tsx
import AppWalletProvider from '@/components/WalletProvider';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <AppWalletProvider>
          {children}
        </AppWalletProvider>
      </body>
    </html>
  );
}
```

### Step 3: Update BettingInterface to Use Wallet

Update `frontend/components/BettingInterface.tsx`:

```tsx
'use client';

import { useState } from 'react';
import { useWallet, useConnection } from '@solana/wallet-adapter-react';
import { WalletMultiButton } from '@solana/wallet-adapter-react-ui';
import {
  PublicKey,
  Transaction,
  SystemProgram,
  LAMPORTS_PER_SOL,
} from '@solana/web3.js';
import { Finalist } from '@/types';

interface BettingInterfaceProps {
  finalist: Finalist;
  onPlaceBet: (finalistId: string, amount: number, signature: string) => Promise<void>;
}

export default function BettingInterface({ finalist, onPlaceBet }: BettingInterfaceProps) {
  const { publicKey, sendTransaction } = useWallet();
  const { connection } = useConnection();
  const [betAmount, setBetAmount] = useState<number>(0.1);
  const [isPlacingBet, setIsPlacingBet] = useState(false);
  const [betPlaced, setBetPlaced] = useState(false);

  const betOptions = [0.1, 0.5, 1.0, 2.5, 5.0];

  const handlePlaceBet = async () => {
    if (!publicKey) {
      alert('Please connect your wallet first!');
      return;
    }

    setIsPlacingBet(true);
    try {
      // Create transaction
      // IMPORTANT: Replace with your actual bet pool wallet address
      const betPoolAddress = new PublicKey(
        process.env.NEXT_PUBLIC_BET_POOL_ADDRESS ||
        '11111111111111111111111111111111' // Placeholder
      );

      const transaction = new Transaction().add(
        SystemProgram.transfer({
          fromPubkey: publicKey,
          toPubkey: betPoolAddress,
          lamports: betAmount * LAMPORTS_PER_SOL,
        })
      );

      // Send transaction
      const signature = await sendTransaction(transaction, connection);

      // Wait for confirmation
      await connection.confirmTransaction(signature, 'confirmed');

      // Record bet on backend
      await onPlaceBet(finalist.story.story_id, betAmount, signature);

      setBetPlaced(true);
      setTimeout(() => setBetPlaced(false), 3000);
    } catch (error) {
      console.error('Bet placement failed:', error);
      alert('Bet placement failed. Please try again.');
    } finally {
      setIsPlacingBet(false);
    }
  };

  if (!publicKey) {
    return (
      <div className="bg-white border-2 border-black p-4 text-center">
        <div className="mb-3 text-xs uppercase text-black opacity-60">
          Connect wallet to bet
        </div>
        <WalletMultiButton className="!bg-black !text-white !border-2 !border-black !font-bold !text-xs !uppercase !tracking-wide" />
      </div>
    );
  }

  // ... rest of component (same as before)
}
```

---

## Backend Implementation

### Step 1: Create Betting Service

Create `backend/services/betting.py`:

```python
"""
Betting Service - Track bets and manage payouts
"""

from typing import Dict, List, Optional
from pydantic import BaseModel
from datetime import datetime
import json
import os


class Bet(BaseModel):
    """Represents a user bet"""
    bet_id: str
    user_wallet: str
    finalist_id: str
    amount_sol: float
    transaction_signature: str
    timestamp: datetime
    status: str = "pending"  # pending, confirmed, won, lost


class BettingPool(BaseModel):
    """Represents the betting pool for a story"""
    finalist_id: str
    total_bets: float
    bet_count: int
    bets: List[Bet] = []


class BettingService:
    """Service for managing bets and payouts"""

    def __init__(self, storage_path: str = "data/bets.json"):
        self.storage_path = storage_path
        self.pools: Dict[str, BettingPool] = {}
        self._load_data()

    def _load_data(self):
        """Load betting data from storage"""
        if os.path.exists(self.storage_path):
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
                for pool_data in data.get('pools', []):
                    pool = BettingPool(**pool_data)
                    self.pools[pool.finalist_id] = pool

    def _save_data(self):
        """Save betting data to storage"""
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        data = {
            'pools': [pool.model_dump() for pool in self.pools.values()]
        }
        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)

    async def place_bet(
        self,
        user_wallet: str,
        finalist_id: str,
        amount_sol: float,
        transaction_signature: str
    ) -> Bet:
        """Record a bet placement"""

        # Verify transaction on Solana (implement with solana-py)
        # await self._verify_transaction(transaction_signature, amount_sol)

        # Create bet record
        bet = Bet(
            bet_id=f"bet_{transaction_signature[:8]}",
            user_wallet=user_wallet,
            finalist_id=finalist_id,
            amount_sol=amount_sol,
            transaction_signature=transaction_signature,
            timestamp=datetime.now(),
            status="confirmed"
        )

        # Add to pool
        if finalist_id not in self.pools:
            self.pools[finalist_id] = BettingPool(
                finalist_id=finalist_id,
                total_bets=0.0,
                bet_count=0
            )

        pool = self.pools[finalist_id]
        pool.bets.append(bet)
        pool.total_bets += amount_sol
        pool.bet_count += 1

        self._save_data()
        return bet

    def get_pool_stats(self, finalist_id: str) -> Optional[BettingPool]:
        """Get betting pool statistics for a finalist"""
        return self.pools.get(finalist_id)

    def get_all_pools(self) -> List[BettingPool]:
        """Get all betting pools"""
        return list(self.pools.values())

    async def distribute_payouts(self, winning_finalist_id: str):
        """Distribute payouts to winners (3x payout)"""
        winning_pool = self.pools.get(winning_finalist_id)
        if not winning_pool:
            return

        # Calculate total pool across all finalists
        total_pool = sum(pool.total_bets for pool in self.pools.values())

        # Distribute 3x to winners
        for bet in winning_pool.bets:
            payout = bet.amount_sol * 3
            # TODO: Send SOL back to user_wallet
            # await self._send_sol(bet.user_wallet, payout)
            bet.status = "won"

        # Mark other bets as lost
        for finalist_id, pool in self.pools.items():
            if finalist_id != winning_finalist_id:
                for bet in pool.bets:
                    bet.status = "lost"

        self._save_data()
```

### Step 2: Add Betting Endpoints

Update `backend/main.py`:

```python
from services.betting import BettingService, Bet
from pydantic import BaseModel

# Initialize betting service
betting_service = BettingService()


class PlaceBetRequest(BaseModel):
    """Request to place a bet"""
    user_wallet: str
    finalist_id: str
    amount_sol: float
    transaction_signature: str


@app.post("/api/bets/place")
async def place_bet(request: PlaceBetRequest):
    """
    Place a bet on a finalist story

    Args:
        request: Bet placement details with Solana transaction signature

    Returns:
        Bet confirmation with bet ID
    """
    try:
        bet = await betting_service.place_bet(
            user_wallet=request.user_wallet,
            finalist_id=request.finalist_id,
            amount_sol=request.amount_sol,
            transaction_signature=request.transaction_signature
        )
        return bet.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Bet placement failed: {str(e)}")


@app.get("/api/bets/pools")
async def get_betting_pools():
    """
    Get all betting pool statistics

    Returns:
        List of betting pools with totals and counts
    """
    pools = betting_service.get_all_pools()
    return [pool.model_dump() for pool in pools]


@app.get("/api/bets/pool/{finalist_id}")
async def get_pool_stats(finalist_id: str):
    """
    Get betting pool stats for a specific finalist

    Args:
        finalist_id: ID of the finalist story

    Returns:
        Betting pool statistics
    """
    pool = betting_service.get_pool_stats(finalist_id)
    if not pool:
        raise HTTPException(status_code=404, detail="Pool not found")
    return pool.model_dump()


@app.post("/api/bets/distribute/{winning_finalist_id}")
async def distribute_payouts(winning_finalist_id: str):
    """
    Distribute payouts to winners (Admin only - add auth!)

    Args:
        winning_finalist_id: ID of the winning finalist

    Returns:
        Payout distribution confirmation
    """
    # TODO: Add admin authentication
    await betting_service.distribute_payouts(winning_finalist_id)
    return {"status": "success", "winner": winning_finalist_id}
```

---

## Environment Variables

### Frontend `.env.local`

```bash
# Solana network (devnet, mainnet-beta)
NEXT_PUBLIC_SOLANA_NETWORK=devnet

# Solana RPC endpoint (or use QuickNode/Helius for better performance)
NEXT_PUBLIC_SOLANA_RPC_URL=https://api.devnet.solana.com

# Bet pool wallet address (create a new Solana wallet for this)
NEXT_PUBLIC_BET_POOL_ADDRESS=YourBetPoolWalletAddress

# Backend API
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend `.env`

```bash
# Solana network
SOLANA_NETWORK=devnet

# Bet pool private key (KEEP SECRET!)
BET_POOL_PRIVATE_KEY=your_private_key_base58

# Anthropic API for story generation
ANTHROPIC_API_KEY=your_anthropic_api_key
```

---

## Testing

### 1. Get Devnet SOL

For testing on devnet, get free SOL from the faucet:

```bash
# Using Solana CLI
solana airdrop 2 YOUR_WALLET_ADDRESS --url devnet

# Or use web faucet: https://faucet.solana.com
```

### 2. Test Wallet Connection

1. Install Phantom wallet browser extension
2. Switch network to Devnet in settings
3. Connect wallet on your app
4. Verify wallet address shows in console

### 3. Test Betting Flow

1. Connect wallet
2. Select a finalist
3. Choose bet amount
4. Click "Place Bet"
5. Approve transaction in wallet popup
6. Wait for confirmation
7. Verify bet recorded on backend

---

## Security Considerations

### 1. Transaction Verification

Always verify transactions on-chain:

```python
from solana.rpc.async_api import AsyncClient

async def verify_transaction(signature: str, expected_amount: float):
    """Verify transaction actually happened"""
    client = AsyncClient("https://api.devnet.solana.com")
    tx = await client.get_transaction(signature)

    # Verify amount, sender, receiver
    # ... implementation details
```

### 2. Wallet Security

- **Never store private keys in code**
- Use environment variables for sensitive data
- Keep bet pool wallet separate from operational funds
- Implement multi-sig for large pools

### 3. Rate Limiting

Add rate limiting to prevent spam bets:

```python
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/bets/place")
@limiter.limit("5/minute")
async def place_bet(request: PlaceBetRequest):
    # ... implementation
```

---

## Production Deployment

### 1. Switch to Mainnet

Update environment variables:

```bash
NEXT_PUBLIC_SOLANA_NETWORK=mainnet-beta
NEXT_PUBLIC_SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
```

### 2. Use Premium RPC

For better reliability, use premium RPC providers:

- **QuickNode**: https://www.quicknode.com/
- **Helius**: https://www.helius.dev/
- **Triton**: https://triton.one/

### 3. Set Up Monitoring

Monitor betting activity:

```python
# Add logging
import logging

logging.info(f"Bet placed: {bet.amount_sol} SOL on {bet.finalist_id}")

# Track metrics
# - Total bets placed
# - Total SOL in pool
# - Average bet size
# - Popular finalists
```

---

## Troubleshooting

### "Wallet not connected"
- Check wallet adapter is properly wrapped around app
- Verify wallet extension is installed
- Check browser console for errors

### "Transaction failed"
- Insufficient SOL for transaction + fees
- Network congestion (try again)
- Wrong network (devnet vs mainnet)

### "Bet not recorded"
- Backend may be down
- Transaction not confirmed yet (wait longer)
- Check backend logs for errors

---

## Alternative: Simple x402 Integration

For quicker integration with less custom code, use `@payai/x402-solana-react`:

```tsx
import { X402Paywall } from '@payai/x402-solana-react';

<X402Paywall
  amount={betAmount}
  recipient="YOUR_WALLET_ADDRESS"
  onSuccess={(signature) => {
    onPlaceBet(finalist.story.story_id, betAmount, signature);
  }}
>
  <button>Place Bet</button>
</X402Paywall>
```

This handles wallet connection, transactions, and confirmations automatically.

---

## Resources

- **x402 Protocol**: https://www.x402.org/
- **Solana Wallet Adapter**: https://github.com/solana-labs/wallet-adapter
- **Solana Web3.js**: https://solana-labs.github.io/solana-web3.js/
- **Phantom Wallet**: https://phantom.app/
- **Solana Cookbook**: https://solanacookbook.com/

---

## Next Steps

1. Set up Solana wallet (Phantom or Solflare)
2. Install packages: `npm install @solana/wallet-adapter-react ...`
3. Create bet pool wallet for receiving bets
4. Implement wallet provider wrapper
5. Update BettingInterface with real wallet integration
6. Test on devnet with fake SOL
7. Deploy to production with mainnet

Good luck with your Short Drama IP Factory betting system! 🎰🎬
