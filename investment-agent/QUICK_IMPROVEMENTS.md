# Quick Performance Improvements

## 🚀 Immediate Actions (5-15 minutes each)

### 1. Switch to Faster LLM Model ⚡

**File**: `agent/agent.py` (line ~176)

**Change**:
```python
# BEFORE
model=LiteLlm(
    model="openrouter/deepseek/deepseek-r1",
    ...
)

# AFTER (Much faster)
model=LiteLlm(
    model="openrouter/google/gemini-2.0-flash-exp",  # 3-5x faster
    # OR
    model="openrouter/anthropic/claude-3.5-sonnet",  # Fast + high quality
    api_key=os.getenv("OPENROUTER_API_KEY"),
    api_base="https://openrouter.ai/api/v1"
)
```

**Expected Improvement**: 10-18s → 3-6s

---

### 2. Optimize React Rendering 🔄

**File**: `src/app/page.tsx`

**Add memoization**:
```typescript
// At top of file
import React, { useState, useEffect, useMemo, useCallback } from "react";

// Wrap InvestmentCard
const InvestmentCard = React.memo(({
  option,
  theme,
  status,
  onToggle,
  disabled = false,
}: {
  option: InvestmentOption;
  theme?: string;
  status?: string;
  onToggle: () => void;
  disabled?: boolean;
}) => {
  // ... existing code
}, (prevProps, nextProps) => {
  return (
    prevProps.option.status === nextProps.option.status &&
    prevProps.disabled === nextProps.disabled
  );
});
```

**Memoize options list**:
```typescript
// In InvestmentFeedback component
const options = useMemo(() => {
  return localOptions.length > 0 ? localOptions : args.options || [];
}, [localOptions, args?.options]);

const enabledCount = useMemo(() => {
  return options.filter((opt: InvestmentOption) => opt.status === "enabled").length;
}, [options]);
```

**Expected Improvement**: Smoother UI, less flickering

---

### 3. Fix State Initialization 🐛

**File**: `src/app/page.tsx` (line ~333)

**Change**:
```typescript
// BEFORE
useEffect(() => {
  if (localOptions.length === 0 && args?.options) {
    // ...
  }
}, [args?.options, localOptions.length]);

// AFTER
useEffect(() => {
  if (args?.options && localOptions.length === 0) {
    const options = args.options.map((opt: any) => ({
      name: opt.name || "",
      description: opt.description || "",
      riskLevel: opt.riskLevel || "medium",
      minimumAmount: opt.minimumAmount || 0,
      status: opt.status || "enabled",
    }));
    setLocalOptions(options);
  }
}, [args?.options]); // Remove localOptions.length
```

**Expected Improvement**: Prevents unnecessary re-initializations

---

### 4. Add Loading Indicator ⏳

**File**: `src/app/page.tsx`

**Add to InvestmentFeedback component**:
```typescript
// After line 346
if (!args?.options || args.options.length === 0) {
  // Show loading if status is executing
  if (status === "executing") {
    return (
      <InvestmentContainer theme={theme}>
        <div className="flex flex-col items-center justify-center p-8">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
          <p className="text-gray-600">Generating investment options...</p>
        </div>
      </InvestmentContainer>
    );
  }
  return <></>;
}
```

**Expected Improvement**: Better UX, users know something is happening

---

### 5. Shorten Agent Instruction 📝

**File**: `agent/agent.py` (line ~184)

**Simplify instruction**:
```python
instruction=f"""
You are an investment advisor. Generate 5-7 investment options.

Each option needs:
- name: Investment type name
- description: Brief description (max 50 words)
- riskLevel: "low", "medium", or "high"
- minimumAmount: Minimum investment in USD
- status: "enabled"

Consider user's budget and preferences. Provide diverse options.
"""
```

**Expected Improvement**: Faster LLM processing, less tokens

---

## 📊 Combined Impact

After implementing all 5 improvements:

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Response Time | 10-18s | 3-6s | **60-70% faster** |
| UI Smoothness | Occasional flicker | Smooth | **Better UX** |
| User Feedback | None | Loading indicator | **Better UX** |
| Re-renders | Many | Optimized | **Better performance** |

---

## 🎯 Implementation Order

1. **Switch Model** (5 min) - Biggest impact
2. **Add Loading Indicator** (10 min) - Immediate UX improvement
3. **Fix State Init** (2 min) - Quick bug fix
4. **Optimize Rendering** (15 min) - Performance boost
5. **Shorten Instruction** (5 min) - Small improvement

**Total Time**: ~40 minutes
**Expected Result**: 60-70% faster, much better UX

