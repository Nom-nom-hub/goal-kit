# Week 2 Development Plan - ProjectAnalyzer & Status Command

**Duration**: 5 working days (Dec 8-12, 2025)  
**Goal**: Extract ProjectAnalyzer class, implement /goalkit.status command  
**Outcome**: 2 new modules, 30+ new tests, 20+ new lines of integrated functionality

---

## Current Status (End of Week 1)

✅ **Completed**:
- agents.py (100% coverage, 15 tests)
- models.py (100% coverage, 15 tests)
- templates.py (79% coverage, 21 tests)
- commands/ structure (init, check modules)
- 51 total tests passing

✅ **Branch**: refactor/modular-architecture (5 commits)

---

## Week 2 Architecture

### New Modules

#### 1. analyzer.py (NEW)
**Purpose**: Analyze goal-kit projects and extract project state  
**Expected Size**: 150-200 lines  
**Tests**: 15-20 tests

**Class: ProjectAnalyzer**
```python
class ProjectAnalyzer:
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.project = self._load_project()
    
    def _load_project(self) -> Project:
        """Load project metadata from .goalkit directory"""
        pass
    
    def analyze_goals(self) -> List[Goal]:
        """Parse .goalkit/goals/*.md files"""
        pass
    
    def count_completion(self) -> float:
        """Calculate overall project completion %"""
        pass
    
    def get_health_score(self) -> float:
        """Calculate health score (0-100)"""
        pass
    
    def detect_phase(self) -> str:
        """Determine project phase (setup, active, execution, etc)"""
        pass
```

**Helper Functions**:
- `parse_goal_file()`: Extract goal data from markdown
- `extract_metrics()`: Find metrics in goal files
- `calculate_score()`: Health scoring algorithm

#### 2. commands/status.py (NEW)
**Purpose**: Display project status and health information  
**Expected Size**: 100-150 lines  
**Tests**: 10-15 tests

**Function: status()**
```python
def status(
    project_path: Optional[Path] = None,
    verbose: bool = False,
    json_output: bool = False,
) -> None:
    """Show project status, health, and progress"""
    # Use ProjectAnalyzer to get state
    # Format and display results
    pass
```

**Output**:
- Project name and location
- Phase (setup, active, execution, complete)
- Health score (0-100)
- Goal completion summary
- Current milestone progress
- Recent milestone achievements
- Next recommended action

---

## Daily Breakdown

### Monday: Analyzer Foundation

#### Morning (3 hours)
- [ ] Create analyzer.py skeleton
- [ ] Define ProjectAnalyzer class
- [ ] Stub methods with type hints
- [ ] Add docstrings
- [ ] Create first test file

**Work Items**:
- [ ] Create `src/goalkeeper_cli/analyzer.py` (skeleton)
- [ ] Add `ProjectAnalyzer` class
- [ ] Add `Project` loading logic
- [ ] Add `Goal` parsing logic
- [ ] Add health calculation

#### Afternoon (2 hours)
- [ ] Parse .goalkit project structure
- [ ] Load project.json metadata
- [ ] Read goals directory structure
- [ ] Calculate basic completion %

#### Evening (1 hour)
- [ ] Review code
- [ ] Run basic tests
- [ ] Commit: `feat: ProjectAnalyzer foundation`

---

### Tuesday: Analyzer Implementation

#### Morning (3 hours)
- [ ] Implement goal parsing from markdown
- [ ] Extract metrics and criteria
- [ ] Implement phase detection
- [ ] Implement health score calculation

#### Afternoon (2 hours)
- [ ] Add analysis helpers
- [ ] Test with sample projects
- [ ] Fix edge cases
- [ ] Performance optimization

#### Evening (1 hour)
- [ ] Create comprehensive tests
- [ ] Aim for 80%+ coverage
- [ ] Commit: `feat: ProjectAnalyzer complete`

---

### Wednesday: Status Command

#### Morning (3 hours)
- [ ] Create commands/status.py
- [ ] Implement status() function
- [ ] Add output formatting
- [ ] Add Rich panels/tables for display

#### Afternoon (2 hours)
- [ ] Add --verbose flag support
- [ ] Add --json output option
- [ ] Add error handling
- [ ] Test with sample projects

#### Evening (1 hour)
- [ ] Create tests for status command
- [ ] Fix any failures
- [ ] Commit: `feat: /goalkit.status command`

---

### Thursday: Integration & Testing

#### Morning (2 hours)
- [ ] Wire status command to CLI app
- [ ] Test actual CLI invocation
- [ ] Fix import issues

#### Afternoon (3 hours)
- [ ] Integration tests
- [ ] Full test suite: `pytest tests/ -v`
- [ ] Coverage analysis
- [ ] Fix gaps

#### Evening (1 hour)
- [ ] Performance testing
- [ ] Documentation review
- [ ] Commit: `chore: integration tests`

---

### Friday: Polish & Documentation

#### Morning (2 hours)
- [ ] Final code review
- [ ] Update AGENTS.md with new modules
- [ ] Update type hints

#### Afternoon (2 hours)
- [ ] Create WEEK2_SUMMARY.md
- [ ] Final test run
- [ ] Performance benchmarks

#### Evening (1 hour)
- [ ] Prepare PR materials
- [ ] Final commit
- [ ] Push to GitHub

---

## Test Strategy

### Unit Tests (analyzer.py)
- TestProjectAnalyzer: 8-10 tests
  - Initialization
  - Goal parsing
  - Completion calculation
  - Health scoring
  - Phase detection
  - Error handling

- TestAnalysisHelpers: 5-7 tests
  - Parse goal file
  - Extract metrics
  - Calculate score
  - Edge cases

### Integration Tests (commands/status.py)
- TestStatusCommand: 5-7 tests
  - Status display
  - Verbose output
  - JSON output
  - Error cases
  - Empty project

### CLI Tests
- Test actual `goalkeeper status` command
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
✅ 25+ new tests  
✅ 80%+ coverage for new modules  
✅ All tests passing  
✅ Zero regressions  

### Architecture
✅ Clean separation of analyzer/commands  
✅ Uses existing models (Project, Goal, etc)  
✅ Integrates with CLI framework  
✅ Ready for additional commands  

### Documentation
✅ AGENTS.md updated  
✅ WEEK2_SUMMARY.md created  
✅ Code has comprehensive docstrings  
✅ Examples in commit messages  

---

## Expected Outcomes

### By End of Week 2

**New Code**:
- analyzer.py: ~150-200 lines
- commands/status.py: ~100-150 lines
- 25-30 tests: ~400-500 lines

**Commits**:
1. feat: ProjectAnalyzer foundation
2. feat: ProjectAnalyzer complete
3. feat: /goalkit.status command
4. chore: integration tests
5. docs: Week 2 summary

**Test Results**:
- 76+ total tests passing (51 from Week 1 + 25 new)
- Coverage: 22% overall (up from 20%)
- Zero regressions

**Feature Added**:
- `/goalkit.status` command fully functional
- Projects can be analyzed for health/progress
- Users can see current state without opening files

---

## Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| Parsing .md files fragile | Use regex patterns from existing code |
| Health scoring too complex | Keep algorithm simple, add comments |
| Status output cluttered | Use Rich formatting, test readability |
| Performance with large projects | Stream file reads, lazy evaluation |
| Goal file format inconsistency | Document assumptions in docstrings |

---

## Dependencies & Resources

**Existing Modules**:
- models.py (Project, Goal, Milestone, Task)
- agents.py (AgentRegistry)
- helpers.py (StepTracker, etc)
- __init__.py (CLI framework, utilities)

**No New External Dependencies** needed

**Test Resources**:
- Use sample projects from templates/
- Create synthetic test data
- Mock file I/O where needed

---

## Next Steps (Week 3+)

After Week 2:
- [ ] Extract ExecutionTracker class (Week 3)
- [ ] Implement /goalkit.milestones command
- [ ] Add metrics tracking system
- [ ] Continue reducing __init__.py

---

## Notes

- Keep focus on clean extraction, not perfection
- Test coverage more important than feature completeness
- Document assumptions and design decisions
- Commit frequently (daily or after each module)
- Review code before moving to next section

