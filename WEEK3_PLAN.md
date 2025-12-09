# Week 3 Development Plan - ExecutionTracker & Milestones Command

**Duration**: 5 working days (Dec 16-20, 2025)  
**Goal**: Extract ExecutionTracker class, implement /goalkit.milestones command  
**Outcome**: 2 new modules, 30+ new tests, continued modular architecture

---

## Current Status (End of Week 2)

✅ **Completed**:
- agents.py (100% coverage, 15 tests)
- models.py (100% coverage, 15 tests)
- templates.py (79% coverage, 21 tests)
- analyzer.py (99% coverage, 23 tests) ← NEW
- commands/status.py (100% coverage, 33 tests) ← NEW
- 96 total tests passing
- refactor/modular-architecture branch (8 commits)

✅ **Architecture**:
- Clean command pattern established
- ProjectAnalyzer module working well
- Status command fully integrated
- Zero regressions

---

## Week 3 Architecture

### New Modules

#### 1. execution.py (NEW)
**Purpose**: Track goal execution progress and milestone completion  
**Expected Size**: 250-350 lines  
**Tests**: 15-20 tests

**Class: ExecutionTracker**
```python
class ExecutionTracker:
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.project = self._load_project()
    
    def track_milestone(self, goal_id: str, milestone: str) -> None:
        """Mark milestone as completed"""
        pass
    
    def get_milestone_history(self) -> List[MilestoneRecord]:
        """Get execution history"""
        pass
    
    def update_goal_progress(self, goal_id: str, percent: int) -> None:
        """Update goal completion percentage"""
        pass
    
    def get_execution_stats(self) -> ExecutionStats:
        """Get execution statistics and metrics"""
        pass
```

**Helper Functions**:
- `load_milestones()`: Load milestone data from .goalkit/milestones
- `save_milestone_record()`: Persist milestone completion to history
- `calculate_velocity()`: Track completion velocity
- `estimate_completion()`: Project completion date

#### 2. commands/milestones.py (NEW)
**Purpose**: Display milestone progress and execution history  
**Expected Size**: 120-150 lines  
**Tests**: 10-15 tests

**Function: milestones()**
```python
def milestones(
    project_path: Optional[Path] = None,
    goal_id: Optional[str] = None,
    completed_only: bool = False,
    json_output: bool = False,
) -> None:
    """Show milestone progress and execution history"""
    # Use ExecutionTracker to get milestone data
    # Format and display results
    pass
```

**Output**:
- Milestone table with status
- Completion date for each milestone
- Goal-specific milestone filter
- Execution velocity metrics
- Recent milestone achievements
- Next milestone due

---

## Daily Breakdown

### Monday: ExecutionTracker Foundation

#### Morning (3 hours)
- [ ] Create execution.py skeleton
- [ ] Define ExecutionTracker class
- [ ] Add docstrings and type hints
- [ ] Create first test file

**Work Items**:
- [ ] Create `src/goalkeeper_cli/execution.py`
- [ ] Add `ExecutionTracker` class
- [ ] Add milestone loading logic
- [ ] Add execution tracking methods
- [ ] Add helper functions

#### Afternoon (2 hours)
- [ ] Parse .goalkit/milestones directory
- [ ] Load milestone completion records
- [ ] Calculate execution statistics
- [ ] Handle missing milestone data

#### Evening (1 hour)
- [ ] Review code
- [ ] Run basic tests
- [ ] Commit: `feat: ExecutionTracker foundation`

---

### Tuesday: ExecutionTracker Implementation

#### Morning (3 hours)
- [ ] Implement milestone tracking methods
- [ ] Implement progress update logic
- [ ] Implement velocity calculation
- [ ] Implement completion estimation

#### Afternoon (2 hours)
- [ ] Add execution history tracking
- [ ] Test with sample projects
- [ ] Fix edge cases
- [ ] Optimize milestone data storage

#### Evening (1 hour)
- [ ] Create comprehensive tests
- [ ] Aim for 80%+ coverage
- [ ] Commit: `feat: ExecutionTracker complete`

---

### Wednesday: Milestones Command

#### Morning (3 hours)
- [ ] Create commands/milestones.py
- [ ] Implement milestones() function
- [ ] Add milestone table formatting
- [ ] Add Rich panels for display

#### Afternoon (2 hours)
- [ ] Add --goal-id filter
- [ ] Add --completed-only flag
- [ ] Add --json output
- [ ] Test with sample projects

#### Evening (1 hour)
- [ ] Create tests for milestones command
- [ ] Fix any failures
- [ ] Commit: `feat: /goalkit.milestones command`

---

### Thursday: Integration & Testing

#### Morning (2 hours)
- [ ] Wire milestones command to CLI app
- [ ] Test actual CLI invocation
- [ ] Fix import issues

#### Afternoon (3 hours)
- [ ] Integration tests with realistic data
- [ ] Full test suite: `pytest tests/ -v`
- [ ] Coverage analysis
- [ ] Performance testing

#### Evening (1 hour)
- [ ] Integration tests complete
- [ ] Commit: `test: integration tests for Week 3`

---

### Friday: Polish & Documentation

#### Morning (2 hours)
- [ ] Final code review
- [ ] Update AGENTS.md with new modules
- [ ] Update type hints

#### Afternoon (2 hours)
- [ ] Create WEEK3_SUMMARY.md
- [ ] Final test run
- [ ] Verify no regressions

#### Evening (1 hour)
- [ ] Prepare PR materials
- [ ] Final commit
- [ ] Plan Week 4

---

## Test Strategy

### Unit Tests (execution.py)
- TestExecutionTracker: 8-10 tests
  - Initialization
  - Milestone tracking
  - Progress updates
  - Velocity calculation
  - Estimation logic
  - Error handling

- TestExecutionHelpers: 5-7 tests
  - Load milestones
  - Save records
  - Calculate metrics
  - Edge cases

### Integration Tests (commands/milestones.py)
- TestMilestonesCommand: 8-10 tests
  - Milestone display
  - Goal filtering
  - Completed-only filter
  - JSON output
  - Empty project
  - Error cases

### CLI Integration Tests
- Test actual `goalkeeper milestones` command
- Test with sample projects
- Test error output

---

## Success Criteria

### Code Quality
✅ Type hints on all new code  
✅ Docstrings in Google style  
✅ Error handling for edge cases  
✅ No external dependency additions  

### Testing
✅ 25-30 new tests  
✅ 80%+ coverage for new modules  
✅ All tests passing  
✅ Zero regressions  

### Architecture
✅ Clean separation of tracker/command  
✅ Uses existing models (Goal, Milestone)  
✅ Integrates with CLI framework  
✅ Pattern matches Week 2 modules  

### Documentation
✅ AGENTS.md updated  
✅ WEEK3_SUMMARY.md created  
✅ Code has comprehensive docstrings  
✅ Examples in commit messages  

---

## Expected Outcomes

### By End of Week 3

**New Code**:
- execution.py: ~250-350 lines
- commands/milestones.py: ~120-150 lines
- 25-30 tests: ~400-500 lines

**Commits**:
1. feat: ExecutionTracker foundation
2. feat: ExecutionTracker complete
3. feat: /goalkit.milestones command
4. test: integration tests
5. docs: Week 3 summary

**Test Results**:
- 120+ total tests passing (96 from Week 1-2 + 25-30 new)
- Coverage: 24%+ overall (up from 22%)
- Zero regressions

**Features Added**:
- `/goalkit.milestones` command fully functional
- Milestone tracking system
- Execution velocity metrics
- Completion estimation

---

## Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| Milestone data structure complexity | Use simple JSON format like Week 2 |
| Velocity calculation edge cases | Test with various completion patterns |
| Command filtering logic | Comprehensive filter testing |
| Integration with analyzer data | Verify data consistency with analyzer |
| Large project performance | Use efficient data loading |

---

## Dependencies & Resources

**Existing Modules**:
- models.py (Project, Goal, Milestone, Task)
- analyzer.py (ProjectAnalyzer, AnalysisResult)
- commands/status.py (Status command pattern)
- helpers.py (StepTracker, Rich utilities)

**No New External Dependencies** needed

**Test Resources**:
- Use sample projects from Week 2
- Create synthetic milestone data
- Mock file I/O where needed

---

## Next Steps (Week 4+)

After Week 3:
- [ ] Extract metrics tracking system
- [ ] Implement /goalkit.metrics command
- [ ] Reduce __init__.py further (target: 400 lines)
- [ ] Begin task management module

---

## Notes

- Follow Week 2 patterns established
- Aim for 80%+ coverage
- Test early and often
- Commit frequently
- Document architectural decisions
- Keep modules focused and testable

---

## Comparison to Week 2

| Aspect | Week 2 | Week 3 (Planned) |
|--------|--------|-----------------|
| Source code | 392 lines | 370-500 lines |
| Tests | 66 tests | 25-30 tests |
| Coverage | 99.5% | 80%+ |
| Commits | 8 | 5 |
| Days | 5 | 5 |
| Modules | 2 | 2 |

**Expected**: Slightly more complex (milestone tracking) but similar scope and effort.
