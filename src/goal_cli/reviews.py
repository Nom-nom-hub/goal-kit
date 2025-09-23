"""
Review process automation module for the goal-dev-spec system.
Automates review workflows, notifications, and approval tracking.
"""

import os
import yaml
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum

class ReviewStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    APPROVED = "approved"
    REJECTED = "rejected"
    CHANGES_REQUESTED = "changes_requested"

class ReviewType(Enum):
    GOAL = "goal"
    SPECIFICATION = "specification"
    PLAN = "plan"
    TASK = "task"
    CODE = "code"
    SECURITY = "security"
    COMPLIANCE = "compliance"

class ReviewManager:
    """Manages automated review processes and approval workflows."""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.reviews_path = project_path / ".goal" / "reviews"
        self.reviews_path.mkdir(exist_ok=True)
        
        # Load review templates
        self.review_templates = self._load_review_templates()
        
        # Load reviewer assignments
        self.reviewer_assignments = self._load_reviewer_assignments()
    
    def _load_review_templates(self) -> Dict:
        """Load review templates."""
        return {
            "goal": {
                "name": "Goal Review",
                "reviewers": ["tech_lead", "project_owner"],
                "checklist": [
                    "Clear and measurable objectives",
                    "Well-defined success criteria",
                    "Explicit dependencies identified",
                    "Appropriate priority level",
                    "Stakeholder alignment"
                ]
            },
            "specification": {
                "name": "Specification Review",
                "reviewers": ["tech_lead", "domain_expert", "qa_engineer"],
                "checklist": [
                    "Complete user stories",
                    "Testable acceptance criteria",
                    "Functional requirements specified",
                    "Non-functional requirements specified",
                    "Security considerations included",
                    "Edge cases addressed"
                ]
            },
            "plan": {
                "name": "Implementation Plan Review",
                "reviewers": ["tech_lead", "project_owner", "team_lead"],
                "checklist": [
                    "Detailed task breakdown",
                    "Realistic timeline estimates",
                    "Resource allocation identified",
                    "Risk mitigation strategies",
                    "Dependencies properly mapped"
                ]
            },
            "security": {
                "name": "Security Review",
                "reviewers": ["security_engineer", "tech_lead"],
                "checklist": [
                    "Authentication mechanisms defined",
                    "Authorization controls specified",
                    "Data protection measures included",
                    "Input validation requirements",
                    "Secure coding practices followed"
                ]
            },
            "compliance": {
                "name": "Compliance Review",
                "reviewers": ["compliance_officer", "tech_lead"],
                "checklist": [
                    "Regulatory requirements addressed",
                    "Audit trail requirements met",
                    "Data privacy considerations",
                    "Industry standard compliance",
                    "Organizational policy adherence"
                ]
            }
        }
    
    def _load_reviewer_assignments(self) -> Dict:
        """Load reviewer assignments."""
        # In a real implementation, this would load from a configuration file
        return {
            "tech_lead": {
                "name": "Technical Lead",
                "email": "techlead@example.com",
                "roles": ["goal", "specification", "plan", "security", "compliance"]
            },
            "project_owner": {
                "name": "Project Owner",
                "email": "projectowner@example.com",
                "roles": ["goal", "plan"]
            },
            "domain_expert": {
                "name": "Domain Expert",
                "email": "domainexpert@example.com",
                "roles": ["specification"]
            },
            "qa_engineer": {
                "name": "QA Engineer",
                "email": "qaengineer@example.com",
                "roles": ["specification"]
            },
            "security_engineer": {
                "name": "Security Engineer",
                "email": "securityengineer@example.com",
                "roles": ["security"]
            },
            "compliance_officer": {
                "name": "Compliance Officer",
                "email": "complianceofficer@example.com",
                "roles": ["compliance"]
            },
            "team_lead": {
                "name": "Team Lead",
                "email": "teamlead@example.com",
                "roles": ["plan"]
            }
        }
    
    def create_review(self, review_type: ReviewType, artifact_id: str, artifact_data: Dict) -> str:
        """Create a new review for an artifact."""
        review_id = f"rev_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{artifact_id[:8]}"
        
        # Get review template
        template = self.review_templates.get(review_type.value, {})
        
        # Create review record
        review_record = {
            "id": review_id,
            "type": review_type.value,
            "artifact_id": artifact_id,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "status": ReviewStatus.PENDING.value,
            "reviewers": template.get("reviewers", []),
            "checklist": template.get("checklist", []),
            "comments": [],
            "approvals": {},
            "artifact_snapshot": artifact_data
        }
        
        # Save review record
        review_file = self.reviews_path / f"{review_id}.json"
        with open(review_file, 'w') as f:
            json.dump(review_record, f, indent=2)
        
        # Send notifications to reviewers
        self._notify_reviewers(review_id, review_record)
        
        return review_id
    
    def _notify_reviewers(self, review_id: str, review_record: Dict):
        """Notify reviewers about a new review."""
        # In a real implementation, this would send actual notifications
        # For now, we'll just log that notifications would be sent
        print(f"Would notify reviewers for review {review_id}: {review_record['reviewers']}")
    
    def add_comment(self, review_id: str, reviewer: str, comment: str, approved: Optional[bool] = None) -> bool:
        """Add a comment to a review."""
        review_file = self.reviews_path / f"{review_id}.json"
        if not review_file.exists():
            return False
        
        # Load review record
        with open(review_file, 'r') as f:
            review_record = json.load(f)
        
        # Add comment
        comment_record = {
            "reviewer": reviewer,
            "comment": comment,
            "timestamp": datetime.now().isoformat(),
            "approved": approved
        }
        
        review_record["comments"].append(comment_record)
        review_record["updated_at"] = datetime.now().isoformat()
        
        # Update approval status if provided
        if approved is not None:
            review_record["approvals"][reviewer] = approved
            
            # Check if all required approvals are received
            required_reviewers = review_record["reviewers"]
            all_approved = all(review_record["approvals"].get(r, False) for r in required_reviewers)
            
            if all_approved:
                review_record["status"] = ReviewStatus.APPROVED.value
            elif any(not review_record["approvals"].get(r, True) for r in required_reviewers):
                review_record["status"] = ReviewStatus.CHANGES_REQUESTED.value
        
        # Save updated review record
        with open(review_file, 'w') as f:
            json.dump(review_record, f, indent=2)
        
        return True
    
    def get_review(self, review_id: str) -> Optional[Dict]:
        """Get a review by ID."""
        review_file = self.reviews_path / f"{review_id}.json"
        if not review_file.exists():
            return None
        
        with open(review_file, 'r') as f:
            return json.load(f)
    
    def list_reviews(self, status: Optional[ReviewStatus] = None) -> List[Dict]:
        """List all reviews, optionally filtered by status."""
        reviews = []
        
        for review_file in self.reviews_path.glob("*.json"):
            with open(review_file, 'r') as f:
                review_record = json.load(f)
                
            if status is None or review_record["status"] == status.value:
                reviews.append(review_record)
        
        return reviews
    
    def get_pending_reviews_for_reviewer(self, reviewer: str) -> List[Dict]:
        """Get pending reviews for a specific reviewer."""
        all_reviews = self.list_reviews()
        pending_reviews = []
        
        for review in all_reviews:
            if (review["status"] == ReviewStatus.PENDING.value and 
                reviewer in review["reviewers"] and
                reviewer not in review["approvals"]):
                pending_reviews.append(review)
        
        return pending_reviews
    
    def generate_review_report(self) -> str:
        """Generate a review report in markdown format."""
        reviews = self.list_reviews()
        
        report = f"# Review Report\n\n"
        report += f"Generated: {datetime.now().isoformat()}\n\n"
        report += f"Project: {self.project_path}\n\n"
        
        # Summary statistics
        status_counts = defaultdict(int)
        type_counts = defaultdict(int)
        
        for review in reviews:
            status_counts[review["status"]] += 1
            type_counts[review["type"]] += 1
        
        report += "## Summary\n\n"
        report += f"Total Reviews: {len(reviews)}\n\n"
        
        report += "Status Distribution:\n"
        for status, count in status_counts.items():
            report += f"- {status.replace('_', ' ').title()}: {count}\n"
        report += "\n"
        
        report += "Review Type Distribution:\n"
        for review_type, count in type_counts.items():
            report += f"- {review_type.replace('_', ' ').title()}: {count}\n"
        report += "\n"
        
        # Detailed review list
        report += "## Reviews\n\n"
        
        for review in reviews:
            status_icon = {
                "pending": "⏳",
                "in_progress": "🔄",
                "approved": "✅",
                "rejected": "❌",
                "changes_requested": "📝"
            }.get(review["status"], "❓")
            
            report += f"### {status_icon} {review['id']}\n\n"
            report += f"Type: {review['type'].replace('_', ' ').title()}\n"
            report += f"Artifact ID: {review['artifact_id']}\n"
            report += f"Status: {review['status'].replace('_', ' ').title()}\n"
            report += f"Created: {review['created_at']}\n\n"
            
            if review["comments"]:
                report += "Comments:\n"
                for comment in review["comments"]:
                    approved_text = "✅ Approved" if comment.get("approved") else "❌ Rejected" if comment.get("approved") is False else "📝 Comment"
                    report += f"- {approved_text} by {comment['reviewer']} ({comment['timestamp']}): {comment['comment']}\n"
                report += "\n"
        
        return report

# Example usage
if __name__ == "__main__":
    # This is just for testing purposes
    manager = ReviewManager(Path("."))
    print("ReviewManager initialized")