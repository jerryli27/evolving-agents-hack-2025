# Agent Wallets & Privy Integration Guide

How to give each AI writer agent their own wallet and implement agent-to-agent betting.

---

## 🎯 Concept: Agents Betting on Each Other

**The Idea:**
- Each of 5 writer agents has their own SOL wallet
- After each round, agents analyze competitors' stories
- They bet on which story they think will win
- Uses AI reasoning: "Why did Melodrama Maven bet 2 SOL on Plot Twist Master?"
- Creates a meta-game within the competition

**Why This is Cool:**
- Shows AI decision-making in action
- Adds another layer of competition
- Demonstrates AI-to-AI value transfer
- More interesting than just human betting

---

## 🏗️ Architecture

### Data Structure Updates

**Update `frontend/types/index.ts`:**

```typescript
export interface WriterWallet {
  address: string;          // Solana wallet address
  balance: number;          // Current SOL balance
  starting_balance: number; // Initial 10 SOL
  total_bet: number;        // Sum of all bets placed
  total_won: number;        // Sum of all winnings
}

export interface AgentBet {
  bet_id: string;
  from_writer_id: string;   // Who placed the bet
  on_writer_id: string;     // Who they bet on
  amount_sol: number;
  round: number;
  reasoning: string;        // AI's explanation for the bet
  outcome?: 'won' | 'lost'; // Set after round ends
}

export interface Writer {
  writer_id: string;
  name: string;
  description: string;
  style_dna: string;
  total_score: number;
  color: string;
  wallet: WriterWallet;     // ← ADD THIS
  bets_placed: AgentBet[];  // ← ADD THIS
  bets_received: AgentBet[]; // ← ADD THIS (bets on this writer)
}
```

---

## 🔐 Privy Integration (Easiest Wallet Solution)

### Why Privy?

- ✅ **No wallet? No problem** - Creates embedded wallets for users
- ✅ **Email/social login** - Users without crypto can still participate
- ✅ **Cross-chain** - Works with Solana, Ethereum, Base, etc.
- ✅ **Much simpler** than raw Solana Wallet Adapter
- ✅ **Free tier** - 1000 monthly active users

### Setup

**1. Get Privy App ID**
```bash
# Sign up at https://privy.io
# Create new app
# Copy your App ID
```

**2. Install Privy**
```bash
cd frontend
npm install @privy-io/react-auth @privy-io/solana
```

**3. Configure Environment**
```bash
# frontend/.env.local
NEXT_PUBLIC_PRIVY_APP_ID=your_app_id_here
```

**4. Wrap App with PrivyProvider**

Update `frontend/app/layout.tsx`:

```typescript
'use client';

import { PrivyProvider } from '@privy-io/react-auth';
import { solana } from '@privy-io/solana';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <PrivyProvider
          appId={process.env.NEXT_PUBLIC_PRIVY_APP_ID!}
          config={{
            loginMethods: ['wallet', 'email', 'google'],
            appearance: {
              theme: 'light',
              accentColor: '#000000',
              logo: '/logo.png',
            },
            embeddedWallets: {
              createOnLogin: 'users-without-wallets',
              requireUserPasswordOnCreate: false,
            },
            supportedChains: [solana],
          }}
        >
          {children}
        </PrivyProvider>
      </body>
    </html>
  );
}
```

**5. Update BettingInterface Component**

Replace the mock wallet connection with Privy:

```typescript
'use client';

import { usePrivy, useWallets } from '@privy-io/react-auth';
import { useSolanaWallets } from '@privy-io/solana';

export default function BettingInterface({ finalist, onPlaceBet }) {
  const { login, logout, authenticated, user } = usePrivy();
  const { wallets } = useWallets();
  const { createWallet } = useSolanaWallets();

  const [betAmount, setBetAmount] = useState(0.1);
  const [isPlacingBet, setIsPlacingBet] = useState(false);

  const handlePlaceBet = async () => {
    if (!authenticated) {
      await login();
      return;
    }

    setIsPlacingBet(true);

    try {
      // Get Solana wallet
      let solanaWallet = wallets.find(w => w.walletClientType === 'privy');

      if (!solanaWallet) {
        solanaWallet = await createWallet();
      }

      // Place bet transaction
      const signature = await placeBetTransaction(
        solanaWallet,
        finalist.story.story_id,
        betAmount
      );

      await onPlaceBet(finalist.story.story_id, betAmount, signature);

      alert('Bet placed successfully! 🎉');
    } catch (error) {
      console.error('Bet failed:', error);
      alert('Bet failed. Please try again.');
    } finally {
      setIsPlacingBet(false);
    }
  };

  if (!authenticated) {
    return (
      <div className="bg-white border-2 border-black p-4">
        <div className="mb-3 text-xs uppercase text-black opacity-60 text-center">
          Login to place bets
        </div>
        <button
          onClick={login}
          className="w-full py-3 px-4 bg-black text-white border-2 border-black font-bold text-xs uppercase tracking-wide hover:bg-gray-900"
        >
          Login with Wallet / Email
        </button>
      </div>
    );
  }

  return (
    <div className="bg-white border-2 border-black p-3">
      {/* Existing betting UI */}
      <button onClick={handlePlaceBet} disabled={isPlacingBet}>
        {isPlacingBet ? 'PLACING BET...' : 'PLACE BET'}
      </button>

      {/* User info */}
      <div className="mt-2 text-xs text-center">
        <span className="opacity-60">Logged in as:</span> {user?.email || user?.wallet?.address.slice(0, 6)}
        <button onClick={logout} className="ml-2 underline">
          Logout
        </button>
      </div>
    </div>
  );
}

async function placeBetTransaction(wallet: any, finalistId: string, amount: number) {
  // Implementation for Solana transaction
  // See WALLET_INTEGRATION.md for details

  const provider = await wallet.getProvider();
  const connection = new Connection(process.env.NEXT_PUBLIC_SOLANA_RPC!);

  const transaction = new Transaction().add(
    SystemProgram.transfer({
      fromPubkey: new PublicKey(wallet.address),
      toPubkey: new PublicKey(process.env.NEXT_PUBLIC_BET_POOL_ADDRESS!),
      lamports: amount * 1e9, // Convert SOL to lamports
    })
  );

  const signature = await provider.sendTransaction(transaction, connection);
  await connection.confirmTransaction(signature);

  return signature;
}
```

---

## 🤖 Agent Wallet Creation (Backend)

### Generate Wallets for Each Agent

**Backend setup:**

```bash
cd backend
pip install solana anchorpy
```

**Create `backend/services/agent_wallets.py`:**

```python
"""
Agent Wallet Management
Generate and manage wallets for each AI writer agent
"""

from solana.keypair import Keypair
from solders.pubkey import Pubkey
from solana.rpc.async_api import AsyncClient
from typing import Dict, List
import json
import os
from base58 import b58encode, b58decode


class AgentWalletManager:
    """Manage wallets for AI writer agents"""

    def __init__(self):
        self.wallets_file = "data/agent_wallets.json"
        self.starting_balance = 10.0  # 10 SOL per agent
        self.wallets: Dict[str, dict] = {}
        self._load_or_create_wallets()

    def _load_or_create_wallets(self):
        """Load existing wallets or create new ones"""
        if os.path.exists(self.wallets_file):
            with open(self.wallets_file, 'r') as f:
                self.wallets = json.load(f)
        else:
            # Create wallets for 5 writer agents
            writer_ids = ['writer_1', 'writer_2', 'writer_3', 'writer_4', 'writer_5']
            for writer_id in writer_ids:
                self.wallets[writer_id] = self._create_wallet(writer_id)
            self._save_wallets()

    def _create_wallet(self, writer_id: str) -> dict:
        """Create a new Solana wallet for an agent"""
        keypair = Keypair()

        return {
            "writer_id": writer_id,
            "address": str(keypair.pubkey()),
            "private_key": b58encode(bytes(keypair.secret())).decode('utf-8'),
            "balance": self.starting_balance,
            "starting_balance": self.starting_balance,
            "total_bet": 0.0,
            "total_won": 0.0,
        }

    def _save_wallets(self):
        """Save wallets to disk"""
        os.makedirs(os.path.dirname(self.wallets_file), exist_ok=True)
        with open(self.wallets_file, 'w') as f:
            json.dump(self.wallets, f, indent=2)

    def get_wallet(self, writer_id: str) -> dict:
        """Get wallet info for a writer agent"""
        return self.wallets.get(writer_id)

    def get_all_wallets(self) -> List[dict]:
        """Get all agent wallets"""
        return list(self.wallets.values())

    async def fund_wallets(self):
        """Fund all agent wallets with SOL (devnet only)"""
        client = AsyncClient("https://api.devnet.solana.com")

        for writer_id, wallet in self.wallets.items():
            try:
                # Request airdrop (devnet only)
                await client.request_airdrop(
                    Pubkey.from_string(wallet['address']),
                    int(self.starting_balance * 1e9)  # Convert to lamports
                )
                print(f"Funded {writer_id} with {self.starting_balance} SOL")
            except Exception as e:
                print(f"Failed to fund {writer_id}: {e}")

    def update_balance(self, writer_id: str, amount: float):
        """Update wallet balance after bet/win"""
        if writer_id in self.wallets:
            self.wallets[writer_id]['balance'] += amount
            self._save_wallets()

    def record_bet(self, writer_id: str, amount: float):
        """Record that an agent placed a bet"""
        if writer_id in self.wallets:
            self.wallets[writer_id]['total_bet'] += amount
            self.update_balance(writer_id, -amount)

    def record_win(self, writer_id: str, amount: float):
        """Record that an agent won a bet"""
        if writer_id in self.wallets:
            self.wallets[writer_id]['total_won'] += amount
            self.update_balance(writer_id, amount)
```

**Update `backend/main.py`:**

```python
from services.agent_wallets import AgentWalletManager

# Initialize wallet manager
agent_wallet_manager = AgentWalletManager()

@app.get("/api/agents/wallets")
async def get_agent_wallets():
    """Get all agent wallet addresses and balances"""
    return agent_wallet_manager.get_all_wallets()


@app.get("/api/agents/wallets/{writer_id}")
async def get_agent_wallet(writer_id: str):
    """Get specific agent's wallet"""
    wallet = agent_wallet_manager.get_wallet(writer_id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet


@app.post("/api/agents/fund-wallets")
async def fund_agent_wallets():
    """Fund all agent wallets (devnet only)"""
    await agent_wallet_manager.fund_wallets()
    return {"status": "success", "message": "All wallets funded"}
```

---

## 🎲 Agent-to-Agent Betting Logic

### How Agents Decide Who to Bet On

**Create `backend/services/agent_betting.py`:**

```python
"""
Agent Betting Logic
AI agents analyze competitors and place bets
"""

from anthropic import Anthropic
import os
from typing import List, Dict
import json


class AgentBettingService:
    """Service for AI agents to analyze and bet on competitors"""

    def __init__(self):
        self.anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    async def analyze_and_bet(
        self,
        agent_writer_id: str,
        agent_style: str,
        competitors_stories: List[Dict],
        available_balance: float
    ) -> Dict:
        """
        Agent analyzes competitor stories and decides who to bet on

        Returns:
            {
                "bet_on_writer_id": "writer_3",
                "bet_amount": 2.5,
                "reasoning": "Plot Twist Master's story has exceptional novelty..."
            }
        """

        prompt = f"""You are {agent_writer_id}, an AI writer agent with style: {agent_style}.

You just competed in a short drama writing competition. Now you need to analyze your competitors' stories and decide who to bet on for the next round.

Your available balance: {available_balance} SOL

Competitor Stories:
{json.dumps(competitors_stories, indent=2)}

Analyze each story considering:
1. Quality of writing (coherence, pacing, dialogue)
2. Emotional impact and engagement
3. Novelty and creativity
4. Commercial viability for short-form content (TikTok/YouTube Shorts)

Then decide:
- Which writer's story is most likely to win?
- How much should you bet? (Conservative: 10-20% of balance, Aggressive: 30-50%)
- Why did you choose this story?

Return your decision as JSON:
{{
  "bet_on_writer_id": "writer_X",
  "bet_amount": 2.5,
  "reasoning": "Detailed explanation of why you're betting on this story..."
}}

Be analytical and strategic. This is your money on the line!"""

        message = self.anthropic.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )

        response_text = message.content[0].text.strip()

        # Parse JSON response
        if response_text.startswith("```json"):
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif response_text.startswith("```"):
            response_text = response_text.split("```")[1].strip()

        bet_decision = json.loads(response_text)

        # Validate bet amount
        max_bet = available_balance * 0.5  # Max 50% of balance
        bet_decision['bet_amount'] = min(bet_decision['bet_amount'], max_bet)

        return bet_decision
```

**Integrate into Evolution Orchestrator:**

```python
# backend/services/orchestrator.py

async def _run_round(self, round_num: int) -> RoundData:
    """Run a single round with agent betting"""

    # 1. Writers generate stories
    stories = []
    for writer in self.writers:
        story = await writer.generate_story(round_num)
        stories.append(story)

    # 2. Critic scores all stories
    for story in stories:
        scores = await self.critic.score_story(story)
        story.update(scores)

    # 3. Agents bet on competitors (if round < 5)
    if round_num < 5:
        agent_bets = await self._agent_betting_round(stories)
    else:
        agent_bets = []

    return {
        "round": round_num,
        "stories": stories,
        "agent_bets": agent_bets,  # New field!
    }


async def _agent_betting_round(self, stories: List[Dict]) -> List[Dict]:
    """Each agent bets on their favorite competitor"""
    bets = []

    for writer in self.writers:
        # Get competitor stories (exclude own story)
        competitors = [s for s in stories if s['writer_id'] != writer.writer_id]

        # Get wallet balance
        wallet = agent_wallet_manager.get_wallet(writer.writer_id)

        # Agent analyzes and bets
        bet_decision = await agent_betting_service.analyze_and_bet(
            agent_writer_id=writer.writer_id,
            agent_style=writer.style_dna,
            competitors_stories=competitors,
            available_balance=wallet['balance']
        )

        # Record bet
        agent_wallet_manager.record_bet(
            writer.writer_id,
            bet_decision['bet_amount']
        )

        bets.append({
            "from_writer_id": writer.writer_id,
            "on_writer_id": bet_decision['bet_on_writer_id'],
            "amount_sol": bet_decision['bet_amount'],
            "reasoning": bet_decision['reasoning'],
            "round": round_num,
        })

    return bets
```

---

## 🎨 Frontend: Display Agent Bets

**Create `frontend/components/AgentBetsPanel.tsx`:**

```typescript
'use client';

import { AgentBet, Writer } from '@/types';

interface AgentBetsPanelProps {
  bets: AgentBet[];
  writers: Writer[];
  currentRound: number;
}

export default function AgentBetsPanel({ bets, writers, currentRound }: AgentBetsPanelProps) {
  const roundBets = bets.filter(b => b.round === currentRound);

  return (
    <div className="border-2 border-black bg-white mb-6 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
      <div className="border-b-2 border-black bg-black px-4 py-2.5">
        <div className="text-xs md:text-sm font-bold uppercase tracking-wider text-white">
          AGENT BETTING - ROUND {currentRound}
        </div>
      </div>

      <div className="p-4 md:p-6 space-y-4">
        {roundBets.map((bet, idx) => {
          const fromWriter = writers.find(w => w.writer_id === bet.from_writer_id);
          const onWriter = writers.find(w => w.writer_id === bet.on_writer_id);

          return (
            <div key={idx} className="border-2 border-black p-4 bg-gray-50">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-3">
                  <div
                    className="w-3 h-3 border-2 border-black"
                    style={{ backgroundColor: fromWriter?.color }}
                  />
                  <span className="font-bold text-sm uppercase">
                    {fromWriter?.name}
                  </span>
                </div>
                <div className="text-right">
                  <div className="text-xs uppercase opacity-60">BET AMOUNT</div>
                  <div className="font-mono font-bold">{bet.amount_sol} SOL</div>
                </div>
              </div>

              <div className="flex items-center gap-2 mb-3">
                <span className="text-xs opacity-60">BETTING ON:</span>
                <div className="flex items-center gap-2">
                  <div
                    className="w-2 h-2 border border-black"
                    style={{ backgroundColor: onWriter?.color }}
                  />
                  <span className="font-bold text-sm">{onWriter?.name}</span>
                </div>
              </div>

              <div className="bg-white border border-black p-3">
                <div className="text-xs uppercase opacity-60 mb-2">AI REASONING:</div>
                <div className="text-sm font-mono leading-relaxed">
                  "{bet.reasoning}"
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
```

**Add to main page:**

```typescript
// frontend/app/page.tsx

import AgentBetsPanel from '@/components/AgentBetsPanel';

export default function Home() {
  const [selectedRound, setSelectedRound] = useState(5);
  const [agentBets, setAgentBets] = useState<AgentBet[]>([]);

  useEffect(() => {
    // Fetch agent bets from API
    fetch(`${API_URL}/api/rounds`)
      .then(res => res.json())
      .then(rounds => {
        const allBets = rounds.flatMap(r => r.agent_bets || []);
        setAgentBets(allBets);
      });
  }, []);

  return (
    <div>
      {/* Existing UI */}

      {/* Agent Bets Section */}
      <AgentBetsPanel
        bets={agentBets}
        writers={writers}
        currentRound={selectedRound}
      />

      {/* Rest of UI */}
    </div>
  );
}
```

---

## 💰 Payout Distribution

After round 5, distribute winnings:

```python
# backend/services/orchestrator.py

async def _distribute_agent_winnings(self):
    """Distribute winnings to agents who bet correctly"""

    # Get winner
    winner_id = self.finalists[0].writer_id

    # Find all bets on the winner
    winning_bets = [
        bet for bet in self.all_agent_bets
        if bet['on_writer_id'] == winner_id
    ]

    # Pay out 2x
    for bet in winning_bets:
        payout = bet['amount_sol'] * 2
        agent_wallet_manager.record_win(bet['from_writer_id'], payout)
```

---

## ✅ Implementation Checklist

**Backend:**
- [ ] Install solana library
- [ ] Create AgentWalletManager
- [ ] Generate wallets for 5 agents
- [ ] Fund wallets (devnet airdrop)
- [ ] Create AgentBettingService
- [ ] Integrate betting into orchestrator
- [ ] Add wallet API endpoints
- [ ] Implement payout distribution

**Frontend:**
- [ ] Install Privy SDK
- [ ] Configure PrivyProvider
- [ ] Update BettingInterface with Privy
- [ ] Create AgentBetsPanel component
- [ ] Add agent wallet display
- [ ] Show betting reasoning
- [ ] Display wallet balances

**Testing:**
- [ ] Verify agent wallets created
- [ ] Test Privy login flow
- [ ] Test agent betting logic
- [ ] Verify payouts calculated correctly
- [ ] Check UI displays bets properly

---

## 📊 Demo Flow

1. **Show agent wallets** - Each starts with 10 SOL
2. **Round 1 completes** - Agents analyze competitors
3. **Agents place bets** - Show their reasoning
4. **Track balances** - Who's up, who's down
5. **Final round** - Winner takes all
6. **Payouts distributed** - Show final balances

This creates a narrative arc beyond just the writing competition! 🎰🤖
