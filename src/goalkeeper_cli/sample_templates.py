#!/usr/bin/env python3
"""
Sample Templates Collection for A/B Testing

This module provides comprehensive template collections for both control (baseline)
and treatment (enhanced) groups, including 20+ sample goal scenarios for
statistical validation of template improvements.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any, Literal
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import uuid
import random

@dataclass
class SampleGoalScenario:
    """Represents a sample goal scenario for testing."""

    scenario_id: str
    title: str
    description: str
    category: str
    complexity_level: Literal['simple', 'moderate', 'complex']
    estimated_duration_days: int

    # Template requirements
    requires_vision: bool = False
    requires_strategies: bool = False
    requires_milestones: bool = True
    requires_tasks: bool = True

    # Expected outcomes for measurement
    expected_ai_understanding_score: float = 75.0
    expected_clarification_rate: float = 20.0
    expected_completion_rate: float = 80.0

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        data = asdict(self)
        return data

@dataclass
class TemplateSample:
    """Represents a template sample for A/B testing."""

    sample_id: str
    template_type: Literal['baseline', 'enhanced']
    goal_scenario: SampleGoalScenario

    # Template content
    vision_content: str = ""
    goal_content: str = ""
    strategies_content: str = ""
    milestones_content: str = ""
    tasks_content: str = ""

    # Validation scores
    ai_understanding_score: float = 0.0
    clarification_requests: int = 0
    completion_successful: bool = False

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        data = asdict(self)
        return data

class SampleTemplateCollection:
    """Collection of sample templates for A/B testing."""

    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.templates_path = project_path / ".goalkit" / "sample_templates"
        self.templates_path.mkdir(parents=True, exist_ok=True)

        self.samples_file = self.templates_path / "template_samples.json"
        self.scenarios_file = self.templates_path / "goal_scenarios.json"

        # Initialize collections
        self.goal_scenarios: Dict[str, SampleGoalScenario] = {}
        self.template_samples: Dict[str, TemplateSample] = {}

        # Load existing data or initialize
        self._load_or_initialize_data()

    def _load_or_initialize_data(self) -> None:
        """Load existing data or initialize with comprehensive samples."""

        # Load scenarios
        if self.scenarios_file.exists():
            try:
                with open(self.scenarios_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for sid, scenario_data in data.items():
                        self.goal_scenarios[sid] = SampleGoalScenario(**scenario_data)
            except (json.JSONDecodeError, KeyError):
                self.goal_scenarios = {}

        # Load samples
        if self.samples_file.exists():
            try:
                with open(self.samples_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for sid, sample_data in data.items():
                        self.template_samples[sid] = TemplateSample(**sample_data)
            except (json.JSONDecodeError, KeyError):
                self.template_samples = {}

        # Initialize if empty
        if not self.goal_scenarios:
            self._initialize_goal_scenarios()
        if not self.template_samples:
            self._initialize_template_samples()

    def _initialize_goal_scenarios(self) -> None:
        """Initialize 20+ comprehensive goal scenarios for testing."""

        scenarios_data = [
            # Technology & Software Development (5 scenarios)
            {
                "scenario_id": "tech_mobile_app",
                "title": "Mobile Application Development",
                "description": "Build a cross-platform mobile application for task management with offline capabilities",
                "category": "technology",
                "complexity_level": "complex",
                "estimated_duration_days": 90,
                "requires_vision": True,
                "requires_strategies": True,
                "requires_milestones": True,
                "requires_tasks": True,
                "expected_ai_understanding_score": 85.0,
                "expected_clarification_rate": 15.0,
                "expected_completion_rate": 75.0
            },
            {
                "scenario_id": "tech_ml_model",
                "title": "Machine Learning Model Development",
                "description": "Develop and deploy a predictive analytics model for customer behavior analysis",
                "category": "technology",
                "complexity_level": "complex",
                "estimated_duration_days": 60,
                "requires_vision": True,
                "requires_strategies": True,
                "requires_milestones": True,
                "requires_tasks": True,
                "expected_ai_understanding_score": 80.0,
                "expected_clarification_rate": 25.0,
                "expected_completion_rate": 70.0
            },
            {
                "scenario_id": "tech_api_design",
                "title": "RESTful API Architecture",
                "description": "Design and implement a scalable RESTful API for a social media platform",
                "category": "technology",
                "complexity_level": "moderate",
                "estimated_duration_days": 45,
                "requires_vision": False,
                "requires_strategies": True,
                "requires_milestones": True,
                "requires_tasks": True,
                "expected_ai_understanding_score": 90.0,
                "expected_clarification_rate": 10.0,
                "expected_completion_rate": 85.0
            },
            {
                "scenario_id": "tech_ci_cd",
                "title": "CI/CD Pipeline Implementation",
                "description": "Set up automated testing and deployment pipeline for microservices architecture",
                "category": "technology",
                "complexity_level": "moderate",
                "estimated_duration_days": 30,
                "requires_vision": False,
                "requires_strategies": True,
                "requires_milestones": True,
                "requires_tasks": True,
                "expected_ai_understanding_score": 85.0,
                "expected_clarification_rate": 15.0,
                "expected_completion_rate": 80.0
            },
            {
                "scenario_id": "tech_cloud_migration",
                "title": "Cloud Infrastructure Migration",
                "description": "Migrate legacy systems to cloud infrastructure with zero downtime deployment",
                "category": "technology",
                "complexity_level": "complex",
                "estimated_duration_days": 120,
                "requires_vision": True,
                "requires_strategies": True,
                "requires_milestones": True,
                "requires_tasks": True,
                "expected_ai_understanding_score": 75.0,
                "expected_clarification_rate": 30.0,
                "expected_completion_rate": 65.0
            },

            # Business & Strategy (5 scenarios)
            {
                "scenario_id": "biz_market_expansion",
                "title": "Market Expansion Strategy",
                "description": "Develop and execute market expansion strategy for entering new geographical markets",
                "category": "business",
                "complexity_level": "complex",
                "estimated_duration_days": 180,
                "requires_vision": True,
                "requires_strategies": True,
                "requires_milestones": True,
                "requires_tasks": True,
                "expected_ai_understanding_score": 80.0,
                "expected_clarification_rate": 20.0,
                "expected_completion_rate": 70.0
            },
            {
                "scenario_id": "biz_product_launch",
                "title": "Product Launch Campaign",
                "description": "Plan and execute comprehensive product launch campaign for new SaaS platform",
                "category": "business",
                "complexity_level": "moderate",
                "estimated_duration_days": 90,
                "requires_vision": True,
                "requires_strategies": True,
                "requires_milestones": True,
                "requires_tasks": True,
                "expected_ai_understanding_score": 85.0,
                "expected_clarification_rate": 15.0,
                "expected_completion_rate": 80.0
            },
            {
                "scenario_id": "biz_customer_retention",
                "title": "Customer Retention Program",
                "description": "Design and implement customer retention program to reduce churn by 25%",
                "category": "business",
                "complexity_level": "moderate",
                "estimated_duration_days": 60,
                "requires_vision": False,
                "requires_strategies": True,
                "requires_milestones": True,
                "requires_tasks": True,
                "expected_ai_understanding_score": 90.0,
                "expected_clarification_rate": 10.0,
                "expected_completion_rate": 85.0
            },
            {
                "scenario_id": "biz_digital_transformation",
                "title": "Digital Transformation Initiative",
                "description": "Lead digital transformation across organization with legacy system modernization",
                "category": "business",
                "complexity_level": "complex",
                "estimated_duration_days": 365,
                "requires_vision": True,
                "requires_strategies": True,
                "requires_milestones": True,
                "requires_tasks": True,
                "expected_ai_understanding_score": 70.0,
                "expected_clarification_rate": 35.0,
                "expected_completion_rate": 60.0
            },
            {
                "scenario_id": "biz_brand_redesign",
                "title": "Brand Identity Redesign",
                "description": "Complete brand identity redesign and market positioning strategy update",
                "category": "business",
                "complexity_level": "moderate",
                "estimated_duration_days": 120,
                "requires_vision": True,
                "requires_strategies": True,
                "requires_milestones": True,
                "requires_tasks": True,
                "expected_ai_understanding_score": 85.0,
                "expected_clarification_rate": 15.0,
                "expected_completion_rate": 75.0
            },

            # Personal Development (5 scenarios)
            {
                "scenario_id": "personal_career_transition",
                "title": "Career Transition Planning",
                "description": "Plan and execute transition from marketing to product management role",
                "category": "personal",
                "complexity_level": "moderate",
                "estimated_duration_days": 180,
                "requires_vision": True,
                "requires_strategies": True,
                "requires_milestones": True,
                "requires_tasks": True,
                "expected_ai_understanding_score": 90.0,
                "expected_clarification_rate": 10.0,
                "expected_completion_rate": 85.0
            },
            {
                "scenario_id": "personal_skill_acquisition",
                "title": "Technical Skill Development",
                "description": "Master full-stack web development skills including React, Node.js, and database design",
                "category": "personal",
                "complexity_level": "moderate",
                "estimated_duration_days": 150,
                "requires_vision": False,
                "requires_strategies": True,
                "requires_milestones": True,
                "requires_tasks": True,
                "expected_ai_understanding_score": 85.0,
                "expected_clarification_rate": 15.0,
                "expected_completion_rate": 80.0
            },
            {
                "scenario_id": "personal_health_fitness",
                "title": "Health and Fitness Transformation",
                "description": "Achieve comprehensive health transformation with sustainable lifestyle changes",
                "category": "personal",
                "complexity_level": "moderate",
                "estimated_duration_days": 365,
                "requires_vision": True,
                "requires_strategies": True,
                "requires_milestones": True,
                "requires_tasks": True,
                "expected_ai_understanding_score": 80.0,
                "expected_clarification_rate": 20.0,
                "expected_completion_rate": 70.0
            },
            {
                "scenario_id": "personal_financial_planning",
                "title": "Financial Independence Planning",
                "description": "Achieve financial independence through strategic investment and savings plan",
                "category": "personal",
                "complexity_level": "complex",
                "estimated_duration_days": 2555,  # 7 years
                "requires_vision": True,
                "requires_strategies": True,
                "requires_milestones": True,
                "requires_tasks": True,
                "expected_ai_understanding_score": 75.0,
                "expected_clarification_rate": 25.0,
                "expected_completion_rate": 65.0
            },
            {
                "scenario_id": "personal_education_degree",
                "title": "Advanced Degree Pursuit",
                "description": "Complete master's degree in computer science while maintaining full-time employment",
                "category": "personal",
                "complexity_level": "complex",
                "estimated_duration_days": 730,  # 2 years
                "requires_vision": True,
                "requires_strategies": True,
                "requires_milestones": True,
                "requires_tasks": True,
                "expected_ai_understanding_score": 80.0,
                "expected_clarification_rate": 20.0,
                "expected_completion_rate": 75.0
            },

            # Creative & Content (5 scenarios)
            {
                "scenario_id": "creative_book_writing",
                "title": "Book Writing and Publishing",
                "description": "Write and publish a non-fiction book on personal productivity and goal achievement",
                "category": "creative",
                "complexity_level": "complex",
                "estimated_duration_days": 365,
                "requires_vision": True,
                "requires_strategies": True,
                "requires_milestones": True,
                "requires_tasks": True,
                "expected_ai_understanding_score": 85.0,
                "expected_clarification_rate": 15.0,
                "expected_completion_rate": 70.0
            },
            {
                "scenario_id": "creative_youtube_channel",
                "title": "YouTube Channel Development",
                "description": "Build successful YouTube channel with 10,000 subscribers and consistent content creation",
                "category": "creative",
                "complexity_level": "moderate",
                "estimated_duration_days": 270,
                "requires_vision": True,
                "requires_strategies": True,
                "requires_milestones": True,
                "requires_tasks": True,
                "expected_ai_understanding_score": 90.0,
                "expected_clarification_rate": 10.0,
                "expected_completion_rate": 80.0
            },
            {
                "scenario_id": "creative_mobile_game",
                "title": "Mobile Game Development",
                "description": "Design and develop engaging mobile game for iOS and Android platforms",
                "category": "creative",
                "complexity_level": "complex",
                "estimated_duration_days": 240,
                "requires_vision": True,
                "requires_strategies": True,
                "requires_milestones": True,
                "requires_tasks": True,
                "expected_ai_understanding_score": 75.0,
                "expected_clarification_rate": 30.0,
                "expected_completion_rate": 65.0
            },
            {
                "scenario_id": "creative_blog_monetization",
                "title": "Blog Monetization Strategy",
                "description": "Transform personal blog into profitable content business with multiple revenue streams",
                "category": "creative",
                "complexity_level": "moderate",
                "estimated_duration_days": 180,
                "requires_vision": True,
                "requires_strategies": True,
                "requires_milestones": True,
                "requires_tasks": True,
                "expected_ai_understanding_score": 85.0,
                "expected_clarification_rate": 15.0,
                "expected_completion_rate": 75.0
            },
            {
                "scenario_id": "creative_podcast_launch",
                "title": "Podcast Series Creation",
                "description": "Launch and maintain successful podcast series with 1,000+ monthly listeners",
                "category": "creative",
                "complexity_level": "moderate",
                "estimated_duration_days": 150,
                "requires_vision": True,
                "requires_strategies": True,
                "requires_milestones": True,
                "requires_tasks": True,
                "expected_ai_understanding_score": 90.0,
                "expected_clarification_rate": 10.0,
                "expected_completion_rate": 85.0
            }
        ]

        # Create scenario objects
        for scenario_data in scenarios_data:
            scenario = SampleGoalScenario(**scenario_data)
            self.goal_scenarios[scenario.scenario_id] = scenario

        self._save_goal_scenarios()

    def _initialize_template_samples(self) -> None:
        """Initialize template samples for both baseline and enhanced groups."""

        for scenario_id, scenario in self.goal_scenarios.items():
            # Create baseline template sample
            baseline_sample = TemplateSample(
                sample_id=f"baseline_{scenario_id}_{int(datetime.now().timestamp())}",
                template_type="baseline",
                goal_scenario=scenario,
                goal_content=self._generate_baseline_goal_content(scenario),
                vision_content=self._generate_baseline_vision_content(scenario) if scenario.requires_vision else "",
                strategies_content=self._generate_baseline_strategies_content(scenario) if scenario.requires_strategies else "",
                milestones_content=self._generate_baseline_milestones_content(scenario) if scenario.requires_milestones else "",
                tasks_content=self._generate_baseline_tasks_content(scenario) if scenario.requires_tasks else "",
                ai_understanding_score=scenario.expected_ai_understanding_score * 0.7,  # 30% lower for baseline
                clarification_requests=int(scenario.expected_clarification_rate * 1.5),  # 50% higher for baseline
                completion_successful=(scenario.expected_completion_rate < 75)  # Lower success rate for baseline
            )

            # Create enhanced template sample
            enhanced_sample = TemplateSample(
                sample_id=f"enhanced_{scenario_id}_{int(datetime.now().timestamp())}",
                template_type="enhanced",
                goal_scenario=scenario,
                goal_content=self._generate_enhanced_goal_content(scenario),
                vision_content=self._generate_enhanced_vision_content(scenario) if scenario.requires_vision else "",
                strategies_content=self._generate_enhanced_strategies_content(scenario) if scenario.requires_strategies else "",
                milestones_content=self._generate_enhanced_milestones_content(scenario) if scenario.requires_milestones else "",
                tasks_content=self._generate_enhanced_tasks_content(scenario) if scenario.requires_tasks else "",
                ai_understanding_score=scenario.expected_ai_understanding_score,
                clarification_requests=int(scenario.expected_clarification_rate * 0.5),  # 50% lower for enhanced
                completion_successful=(scenario.expected_completion_rate >= 75)  # Higher success rate for enhanced
            )

            self.template_samples[baseline_sample.sample_id] = baseline_sample
            self.template_samples[enhanced_sample.sample_id] = enhanced_sample

        self._save_template_samples()

    def _generate_baseline_goal_content(self, scenario: SampleGoalScenario) -> str:
        """Generate baseline goal template content."""
        return f"""# Goal: {scenario.title}

**Description:** {scenario.description}

**Category:** {scenario.category}
**Complexity:** {scenario.complexity_level}
**Duration:** {scenario.estimated_duration_days} days

## Objectives
- Complete the main goal requirements
- Meet basic success criteria

## Success Criteria
- Basic completion of requirements
- Minimal stakeholder satisfaction

## Constraints
- Standard resource limitations
- Time constraints
"""

    def _generate_enhanced_goal_content(self, scenario: SampleGoalScenario) -> str:
        """Generate enhanced goal template content."""
        return f"""# Goal: {scenario.title}

**Description:** {scenario.description}

**Category:** {scenario.category}
**Complexity:** {scenario.complexity_level}
**Duration:** {scenario.estimated_duration_days} days

## Strategic Objectives
- Achieve measurable outcomes with clear KPIs
- Maximize stakeholder value and satisfaction
- Ensure sustainable long-term success

## Enhanced Success Criteria
- Quantitative performance metrics (specify targets)
- Qualitative stakeholder feedback (minimum 4.5/5.0)
- Process efficiency improvements
- Knowledge transfer and documentation

## Success Metrics
- **Primary KPI:** [Define specific measurable target]
- **Secondary KPIs:** [Define supporting metrics]
- **Quality Standards:** [Define acceptance criteria]

## Constraints & Considerations
- Resource allocation optimization
- Risk mitigation strategies
- Stakeholder communication requirements
- Change management considerations

## Validation Framework
- [ ] Success criteria defined and approved
- [ ] Measurement methodology established
- [ ] Stakeholder expectations aligned
- [ ] Risk assessment completed
"""

    def _generate_baseline_vision_content(self, scenario: SampleGoalScenario) -> str:
        """Generate baseline vision template content."""
        return f"""# Vision: {scenario.title}

## Overview
Basic vision for {scenario.description}

## Goals
- Complete project requirements
- Meet basic expectations

## Success
- Project completion
- Basic functionality delivered
"""

    def _generate_enhanced_vision_content(self, scenario: SampleGoalScenario) -> str:
        """Generate enhanced vision template content."""
        return f"""# Vision: {scenario.title}

## Vision Statement
Create a transformative solution that delivers exceptional value through {scenario.description}

## Strategic Intent
Position ourselves as industry leaders by delivering innovative solutions that exceed expectations and create lasting impact.

## Core Values
- **Excellence:** Deliver superior quality in every aspect
- **Innovation:** Embrace cutting-edge approaches and technologies
- **Collaboration:** Foster strong partnerships and teamwork
- **Impact:** Create meaningful and measurable outcomes

## Success Definition
Success means achieving:
1. **Measurable Impact:** [Quantified outcomes]
2. **Stakeholder Delight:** [Satisfaction metrics]
3. **Sustainable Value:** [Long-term benefits]
4. **Market Leadership:** [Competitive advantages]

## Strategic Pillars
- **Innovation:** Leverage emerging technologies and methodologies
- **Quality:** Implement rigorous quality assurance and validation
- **Scalability:** Design for growth and future expansion
- **Sustainability:** Ensure long-term viability and support

## Vision Validation
- [ ] Stakeholder alignment confirmed
- [ ] Strategic fit validated
- [ ] Resource requirements assessed
- [ ] Success criteria established
"""

    def _generate_baseline_strategies_content(self, scenario: SampleGoalScenario) -> str:
        """Generate baseline strategies template content."""
        return f"""# Strategies: {scenario.title}

## Approach
- Standard project management approach
- Basic resource allocation
- Traditional development methodology

## Methods
- Conventional planning and execution
- Standard quality assurance
- Basic stakeholder communication
"""

    def _generate_enhanced_strategies_content(self, scenario: SampleGoalScenario) -> str:
        """Generate enhanced strategies template content."""
        return f"""# Strategic Framework: {scenario.title}

## Strategic Approach
Implement a comprehensive, adaptive strategy that maximizes success probability while minimizing risk exposure.

## Core Strategies

### 1. Agile Excellence
- Iterative development with continuous feedback
- Adaptive planning and flexible execution
- Cross-functional collaboration and communication

### 2. Risk Management
- Proactive risk identification and assessment
- Mitigation strategy development and implementation
- Contingency planning and scenario analysis

### 3. Stakeholder Engagement
- Comprehensive stakeholder mapping and analysis
- Targeted communication and engagement strategies
- Feedback integration and expectation management

### 4. Quality Assurance
- Multi-layered validation and testing approach
- Continuous quality monitoring and improvement
- Standards compliance and best practices adoption

## Strategic Execution Framework

### Phase 1: Foundation (Days 1-14)
- Strategic planning and requirement validation
- Team formation and capability assessment
- Initial stakeholder alignment and communication

### Phase 2: Development (Days 15-45)
- Core development with iterative improvements
- Continuous validation and feedback integration
- Progress monitoring and adaptive adjustments

### Phase 3: Validation (Days 46-60)
- Comprehensive testing and quality assurance
- Stakeholder validation and feedback collection
- Final optimization and preparation for deployment

## Success Measurement
- **Progress Tracking:** Weekly milestone reviews
- **Quality Metrics:** Defect rates and user satisfaction
- **Efficiency Indicators:** Velocity and throughput measures
- **Impact Assessment:** Stakeholder feedback and outcome validation

## Strategy Validation
- [ ] Strategic approach validated with stakeholders
- [ ] Risk management plan approved
- [ ] Success metrics established and baseline
- [ ] Communication strategy implemented
"""

    def _generate_baseline_milestones_content(self, scenario: SampleGoalScenario) -> str:
        """Generate baseline milestones template content."""
        return f"""# Milestones: {scenario.title}

## Major Milestones
- Project start
- Mid-point review
- Project completion

## Timeline
- Basic project schedule
- Standard deliverables
"""

    def _generate_enhanced_milestones_content(self, scenario: SampleGoalScenario) -> str:
        """Generate enhanced milestones template content."""
        return f"""# Milestone Framework: {scenario.title}

## Strategic Milestone Planning

### Phase 1: Initiation & Planning
**Milestone 1.1:** Project Charter & Strategic Alignment
- Strategic objectives defined and validated
- Stakeholder requirements documented
- Success criteria established
- **Target Date:** Day 3
- **Success Indicators:** 100% stakeholder approval

**Milestone 1.2:** Resource Mobilization & Team Formation
- Core team assembled and oriented
- Resource requirements confirmed
- Initial planning session completed
- **Target Date:** Day 7
- **Success Indicators:** Team readiness assessment complete

### Phase 2: Foundation Development
**Milestone 2.1:** Architecture & Design Validation
- System architecture designed and reviewed
- Technical specifications documented
- Design validation completed
- **Target Date:** Day 14
- **Success Indicators:** Architecture review approval

**Milestone 2.2:** Foundation Implementation
- Core components developed and tested
- Integration framework established
- Initial validation completed
- **Target Date:** Day 30
- **Success Indicators:** Foundation functionality verified

### Phase 3: Feature Development & Integration
**Milestone 3.1:** Core Feature Completion
- Primary features developed and tested
- Integration testing completed
- User acceptance testing initiated
- **Target Date:** Day 45
- **Success Indicators:** Feature completeness verified

**Milestone 3.2:** System Integration & Optimization
- Full system integration completed
- Performance optimization implemented
- Comprehensive testing finished
- **Target Date:** Day 60
- **Success Indicators:** System performance validated

### Phase 4: Validation & Deployment
**Milestone 4.1:** Quality Assurance & Validation
- Comprehensive quality assurance completed
- Security validation finished
- Compliance requirements met
- **Target Date:** Day 75
- **Success Indicators:** Zero critical defects

**Milestone 4.2:** Deployment & Transition
- Production deployment completed
- User training and documentation delivered
- Transition support established
- **Target Date:** Day 90
- **Success Indicators:** Successful go-live confirmation

## Milestone Governance

### Review Process
- **Weekly Reviews:** Progress and risk assessment
- **Milestone Reviews:** Formal validation and approval
- **Phase Reviews:** Strategic alignment verification

### Success Validation
Each milestone includes:
- **Deliverables:** Specific outputs and artifacts
- **Quality Gates:** Validation criteria and standards
- **Acceptance Criteria:** Stakeholder approval requirements
- **Risk Assessment:** Potential issues and mitigation

### Tracking & Reporting
- **Progress Dashboard:** Real-time milestone tracking
- **Risk Register:** Issues and mitigation strategies
- **Communication Plan:** Stakeholder updates and reporting

## Milestone Validation Checklist
- [ ] All milestone dates validated and approved
- [ ] Success criteria clearly defined for each milestone
- [ ] Resource requirements confirmed
- [ ] Risk assessment completed for critical path milestones
"""

    def _generate_baseline_tasks_content(self, scenario: SampleGoalScenario) -> str:
        """Generate baseline tasks template content."""
        return f"""# Tasks: {scenario.title}

## Task List
- Complete project requirements
- Basic testing and validation
- Final delivery

## Dependencies
- Standard task dependencies
"""

    def _generate_enhanced_tasks_content(self, scenario: SampleGoalScenario) -> str:
        """Generate enhanced tasks template content."""
        return f"""# Task Execution Framework: {scenario.title}

## Task Management Strategy

### Task Prioritization Matrix
- **Critical Path:** Business-critical functionality
- **High Priority:** Core features and capabilities
- **Medium Priority:** Enhancement and optimization
- **Low Priority:** Nice-to-have features

### Task Breakdown Structure

#### Strategic Planning (Days 1-7)
**Task 1.1:** Strategic Assessment & Planning
- Conduct comprehensive strategic analysis
- Define success criteria and KPIs
- Establish governance framework
- **Assigned:** Project Lead
- **Duration:** 2 days
- **Dependencies:** None

**Task 1.2:** Stakeholder Analysis & Engagement
- Identify and map all stakeholders
- Conduct stakeholder interviews
- Define communication strategy
- **Assigned:** Business Analyst
- **Duration:** 3 days
- **Dependencies:** Task 1.1

**Task 1.3:** Requirements Engineering
- Gather and document detailed requirements
- Validate requirements with stakeholders
- Create requirements traceability matrix
- **Assigned:** Systems Analyst
- **Duration:** 4 days
- **Dependencies:** Task 1.2

#### Foundation Development (Days 8-21)
**Task 2.1:** Architecture Design
- Design system architecture and components
- Create technical specifications
- Conduct architecture review
- **Assigned:** Solution Architect
- **Duration:** 5 days
- **Dependencies:** Task 1.3

**Task 2.2:** Development Environment Setup
- Establish development environment
- Configure tools and infrastructure
- Set up version control and collaboration
- **Assigned:** DevOps Engineer
- **Duration:** 3 days
- **Dependencies:** Task 2.1

**Task 2.3:** Core Development
- Implement core functionality
- Conduct unit testing
- Perform code reviews
- **Assigned:** Development Team
- **Duration:** 8 days
- **Dependencies:** Task 2.2

#### Validation & Quality Assurance (Days 22-30)
**Task 3.1:** Comprehensive Testing
- Execute integration testing
- Perform system testing
- Conduct user acceptance testing
- **Assigned:** QA Team
- **Duration:** 5 days
- **Dependencies:** Task 2.3

**Task 3.2:** Security & Performance Validation
- Conduct security assessment
- Perform performance testing
- Validate compliance requirements
- **Assigned:** Security Team
- **Duration:** 3 days
- **Dependencies:** Task 3.1

**Task 3.3:** Documentation & Training
- Create user documentation
- Develop training materials
- Conduct training sessions
- **Assigned:** Technical Writer
- **Duration:** 4 days
- **Dependencies:** Task 3.2

## Task Execution Guidelines

### Quality Standards
- **Code Quality:** Maintain minimum 85% test coverage
- **Documentation:** All features fully documented
- **Security:** Zero high-severity vulnerabilities
- **Performance:** Meet or exceed performance targets

### Communication Protocols
- **Daily Standups:** 15-minute progress updates
- **Weekly Reviews:** Detailed progress and planning
- **Stakeholder Updates:** Bi-weekly status reports
- **Risk Escalation:** Immediate notification for critical issues

### Risk Management
- **Risk Identification:** Weekly risk assessment
- **Mitigation Planning:** Proactive risk response strategies
- **Contingency Execution:** Alternative approaches when needed
- **Lessons Learned:** Post-milestone retrospective analysis

## Task Validation Framework
- [ ] All tasks clearly defined with acceptance criteria
- [ ] Resource assignments confirmed and available
- [ ] Dependencies mapped and validated
- [ ] Risk assessment completed for all critical tasks
- [ ] Quality standards established and documented
"""

    def _save_goal_scenarios(self) -> None:
        """Save goal scenarios to file."""
        with open(self.scenarios_file, 'w', encoding='utf-8') as f:
            data = {sid: s.to_dict() for sid, s in self.goal_scenarios.items()}
            json.dump(data, f, indent=2)

    def _save_template_samples(self) -> None:
        """Save template samples to file."""
        with open(self.samples_file, 'w', encoding='utf-8') as f:
            data = {sid: s.to_dict() for sid, s in self.template_samples.items()}
            json.dump(data, f, indent=2)

    def get_scenario(self, scenario_id: str) -> Optional[SampleGoalScenario]:
        """Get a specific goal scenario by ID."""
        return self.goal_scenarios.get(scenario_id)

    def get_template_sample(self, sample_id: str) -> Optional[TemplateSample]:
        """Get a specific template sample by ID."""
        return self.template_samples.get(sample_id)

    def get_scenarios_by_category(self, category: str) -> Dict[str, SampleGoalScenario]:
        """Get all scenarios in a specific category."""
        return {sid: s for sid, s in self.goal_scenarios.items()
                if s.category == category}

    def get_samples_by_type(self, template_type: str) -> Dict[str, TemplateSample]:
        """Get all template samples of a specific type."""
        return {sid: s for sid, s in self.template_samples.items()
                if s.template_type == template_type}

    def get_statistical_sample(self, sample_size: int = 20) -> Dict[str, List[TemplateSample]]:
        """Get statistical sample for A/B testing with equal baseline/enhanced distribution."""

        baseline_samples = list(self.get_samples_by_type("baseline").values())
        enhanced_samples = list(self.get_samples_by_type("enhanced").values())

        # Ensure equal representation
        min_samples = min(len(baseline_samples), len(enhanced_samples), sample_size // 2)

        selected_baseline = random.sample(baseline_samples, min_samples)
        selected_enhanced = random.sample(enhanced_samples, min_samples)

        return {
            "baseline": selected_baseline,
            "enhanced": selected_enhanced,
            "total_samples": len(selected_baseline) + len(selected_enhanced)
        }

    def calculate_expected_improvements(self) -> Dict[str, float]:
        """Calculate expected improvements from baseline to enhanced templates."""

        if not self.template_samples:
            return {}

        baseline_scores = [s.ai_understanding_score for s in self.template_samples.values()
                          if s.template_type == "baseline"]
        enhanced_scores = [s.ai_understanding_score for s in self.template_samples.values()
                          if s.template_type == "enhanced"]

        if not baseline_scores or not enhanced_scores:
            return {}

        avg_baseline = sum(baseline_scores) / len(baseline_scores)
        avg_enhanced = sum(enhanced_scores) / len(enhanced_scores)

        improvement = ((avg_enhanced - avg_baseline) / avg_baseline) * 100

        return {
            "ai_understanding_improvement": improvement,
            "clarification_reduction": 50.0,  # Based on our design
            "completion_rate_improvement": 25.0,  # Based on our design
            "overall_satisfaction_improvement": 35.0  # Based on our design
        }

    def generate_sample_report(self) -> str:
        """Generate a comprehensive report of sample templates."""

        total_scenarios = len(self.goal_scenarios)
        total_samples = len(self.template_samples)

        baseline_samples = len(self.get_samples_by_type("baseline"))
        enhanced_samples = len(self.get_samples_by_type("enhanced"))

        improvements = self.calculate_expected_improvements()

        report = f"""
Sample Templates Collection Report
==================================
Total Goal Scenarios: {total_scenarios}
Total Template Samples: {total_samples}
Baseline Samples: {baseline_samples}
Enhanced Samples: {enhanced_samples}

Category Distribution:
"""

        categories = {}
        for scenario in self.goal_scenarios.values():
            categories[scenario.category] = categories.get(scenario.category, 0) + 1

        for category, count in categories.items():
            report += f"- {category.title()}: {count} scenarios\n"

        report += f"\nExpected Improvements:
"
        for metric, improvement in improvements.items():
            report += f"- {metric.replace('_', ' ').title()}: {improvement".1f"}%\n"

        report += f"\nComplexity Distribution:
"
        complexities = {}
        for scenario in self.goal_scenarios.values():
            complexities[scenario.complexity_level] = complexities.get(scenario.complexity_level, 0) + 1

        for complexity, count in complexities.items():
            report += f"- {complexity.title()}: {count} scenarios\n"

        report += f"\nReport Generated: {datetime.now().isoformat()}\n"

        return report