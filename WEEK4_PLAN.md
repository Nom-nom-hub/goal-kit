# Week 4 Development Plan - Metrics Command & Task Management

**Duration**: 5 working days (Dec 23-27, 2025)  
**Goal**: Extract metrics tracking, implement /goalkit.metrics command  
**Outcome**: 2 new modules, 30+ new tests, continued modular architecture

---

## Current Status (End of Week 3)

✅ **Completed**:
- agents.py (100% coverage, 15 tests)
- models.py (100% coverage, 15 tests)
- templates.py (79% coverage, 21 tests)
- analyzer.py (99% coverage, 23 tests)
- commands/status.py (100% coverage, 33 tests)
- execution.py (97% coverage, 33 tests)
- commands/milestones.py (99% coverage, 37 tests)
- 166 total tests passing
- refactor/modular-architecture branch (15 commits)

✅ **Architecture**:
- Tracker + Command pattern fully established
- JSON persistence working well
- Rich console formatting standardized
- No external dependency additions
- Zero regressions across all modules

---

## Week 4 Architecture

### New Modules

#### 1. metrics.py (NEW)
**Purpose**: Track project metrics and progress indicators  
**Expected Size**: 250-350 lines  
**Tests**: 15-20 tests

**Class: MetricsTracker**
```python
class MetricsTracker:
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.execution_dir = project_path / ".goalkit" / "metrics"
    
    def track_metric(self, goal_id: str, metric_name: str, value: float) -> None:
        """Record a metric value"""
        pass
    
    def get_metrics_for_goal(self, goal_id: str) -> Dict[str, List[MetricRecord]]:
        """Get all metrics for a goal"""
        pass
    
    def calculate_health_score(self) -> float:
        """Calculate project health from metrics"""
        pass
    
    def get_metric_trends(self, metric_name: str, days: int = 30) -> Dict[str, float]:
        """Get metric trends over time"""
        pass
```

**Features**:
- Track custom metrics per goal
- Time-series metric data
- Trend analysis
- Health score calculation
- Metric aggregation

#### 2. commands/metrics.py (NEW)
**Purpose**: Display project metrics and health trends  
**Expected Size**: 120-150 lines  
**Tests**: 10-15 tests

**Function: metrics()**
```python
def metrics(
    project_path: Optional[Path] = None,
    goal_id: Optional[str] = None,
    metric_name: Optional[str] = None,
    days: int = 30,
    json_output: bool = False,
) -> None:
    """Show project metrics and health trends"""
    pass
```

**Output**:
- Metric table with values and trends
- Health score indicators
- Trend charts (30/60/90 day views)
- Goal-specific metrics
- Custom metric support

---

## Daily Breakdown

### Monday: Metrics Foundation

#### Morning (3 hours)
- [ ] Create metrics.py skeleton
- [ ] Define MetricsTracker class
- [ ] Add docstrings and type hints
- [ ] Create first test file

#### Afternoon (2 hours)
- [ ] Implement metric tracking methods
- [ ] Implement trend calculation
- [ ] Implement health score calculation
- [ ] Add helper functions

#### Evening (1 hour)
- [ ] Review code
- [ ] Run basic tests
- [ ] Commit: `feat: MetricsTracker foundation`

---

### Tuesday: Metrics Implementation

#### Morning (3 hours)
- [ ] Implement metric persistence
- [ ] Implement trend analysis
- [ ] Implement aggregation logic
- [ ] Handle edge cases

#### Afternoon (2 hours)
- [ ] Add custom metric support
- [ ] Test with sample projects
- [ ] Fix any edge cases
- [ ] Optimize metric calculations

#### Evening (1 hour)
- [ ] Create comprehensive tests
- [ ] Aim for 80%+ coverage
- [ ] Commit: `feat: MetricsTracker complete`

---

### Wednesday: Metrics Command

#### Morning (3 hours)
- [ ] Create commands/metrics.py
- [ ] Implement metrics() function
- [ ] Add metric table formatting
- [ ] Add Rich panels for display

#### Afternoon (2 hours)
- [ ] Add trend visualization
- [ ] Add metric filtering
- [ ] Add --json output
- [ ] Test with sample projects

#### Evening (1 hour)
- [ ] Create tests for metrics command
- [ ] Fix any failures
- [ ] Commit: `feat: /goalkit.metrics command`

---

### Thursday: Integration & Testing

#### Morning (2 hours)
- [ ] Wire metrics command to CLI app
- [ ] Test actual CLI invocation
- [ ] Fix import issues

#### Afternoon (3 hours)
- [ ] Integration tests with realistic data
- [ ] Full test suite: `pytest tests/ -v`
- [ ] Coverage analysis
- [ ] Performance testing

#### Evening (1 hour)
- [ ] Integration tests complete
- [ ] Commit: `test: integration tests for Week 4`

---

### Friday: Polish & Documentation

#### Morning (2 hours)
- [ ] Final code review
- [ ] Update AGENTS.md with new modules
- [ ] Update type hints

#### Afternoon (2 hours)
- [ ] Create WEEK4_SUMMARY.md
- [ ] Final test run
- [ ] Verify no regressions

#### Evening (1 hour)
- [ ] Prepare PR materials
- [ ] Final commit
- [ ] Plan Week 5

---

## Test Strategy

### Unit Tests (metrics.py)
- TestMetricsTracker: 8-10 tests
  - Initialization
  - Metric tracking
  - Trend calculation
  - Health score
  - Aggregation
  - Error handling

- TestMetricHelpers: 5-7 tests
  - Load metrics
  - Save metrics
  - Calculate trends
  - Edge cases

### Integration Tests (commands/metrics.py)
- TestMetricsCommand: 8-10 tests
  - Metric display
  - Goal filtering
  - Date range filtering
  - JSON output
  - Empty project
  - Error cases

### CLI Integration Tests
- Test actual `goalkeeper metrics` command
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
✅ Pattern matches Week 2-3 modules  

### Documentation
✅ AGENTS.md updated  
✅ WEEK4_SUMMARY.md created  
✅ Code has comprehensive docstrings  
✅ Examples in commit messages  

---

## Expected Outcomes

### By End of Week 4

**New Code**:
- metrics.py: ~250-350 lines
- commands/metrics.py: ~120-150 lines
- 25-30 tests: ~400-500 lines

**Commits**:
1. feat: MetricsTracker foundation
2. feat: MetricsTracker complete
3. feat: /goalkit.metrics command
4. test: integration tests
5. docs: Week 4 summary

**Test Results**:
- 25-30 new tests (196+ total)
- Coverage: 28%+ overall (up from 28%)
- Zero regressions

**Features Added**:
- `/goalkit.metrics` command fully functional
- Metric tracking system
- Trend analysis
- Health score calculation
- Custom metric support

---

## Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| Metric data structure complexity | Use simple JSON format like Week 2-3 |
| Trend calculation edge cases | Test with various metric patterns |
| Command filtering logic | Comprehensive filter testing |
| Integration with execution data | Verify data consistency |
| Performance with large datasets | Efficient metric aggregation |

---

## Dependencies & Resources

**Existing Modules**:
- models.py (Project, Goal, Milestone, Task)
- analyzer.py (ProjectAnalyzer, AnalysisResult)
- execution.py (ExecutionTracker, milestone data)
- commands/status.py (Status command pattern)
- commands/milestones.py (Milestones command pattern)
- helpers.py (StepTracker, Rich utilities)

**No New External Dependencies** needed

**Test Resources**:
- Use sample projects from Week 2-3
- Create synthetic metric data
- Mock file I/O where needed

---

## Next Steps (Week 5+)

After Week 4:
- [ ] Extract task management system
- [ ] Implement /goalkit.tasks command
- [ ] Begin reporting and insights module
- [ ] Reduce __init__.py further

---

## Notes

- Follow Week 2-3 patterns established
- Aim for 80%+ coverage
- Test early and often
- Commit frequently
- Document architectural decisions
- Keep modules focused and testable

---

## Comparison to Week 3

| Aspect | Week 3 | Week 4 (Planned) |
|--------|--------|-----------------|
| Source code | 455 lines | 370-500 lines |
| Tests | 70 tests | 25-30 tests |
| Coverage | 97-99% | 80%+ |
| Commits | 5 | 5 |
| Days | 4 | 5 |
| Modules | 2 | 2 |

**Expected**: Similar scope and effort as Week 3.

---

## Success Indicators

- All 25-30 new tests passing
- 80%+ coverage on new modules
- Zero regressions on existing tests
- CLI command working with realistic data
- Clean, well-documented code
- Ready for Week 5 continuation
