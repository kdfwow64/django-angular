from django.contrib import admin
from django.contrib.auth.models import Group


# Model files
from ..models.auth import User, Account, AccountType, UserAccess, UserRole, UserGrant, RoleTracking, AuthenticationType
from ..models.company import Company, CompanyMember, CompanyMemberRole, CompanyMemberRoleType, CompanyAsset, CompanyArtifact, CompanyObjective, CompanyControl, CompanyControlMeasure, CompanyControlMeasurementResult, CompanyControlCapex, CompanyControlCost, CompanyControlCostType, CompanyAssetType, CompanyContact, ContactType, CompanyFinding, CompanyTeam, CompanyLocation, CompanyPlaybook, CompanyPlaybookMember, CompanyPlaybookMemberResponsibility, CompanyPlaybookAction
from ..models.actor import ActorIntent, ActorMotive, Actor
from ..models.audit import Notification, NotificationGroup, AuditChange, Snapshot
from ..models.common import Calendar, CurrencyType, RAGIndicator, EmailTemplate, Expression, IntegerType, Cadence, TimeUnit, TaskStatus, JobTitle, Appetite
from ..models.compliance import Compliance, ComplianceType, ComplianceRequirement, ComplianceVersion, KillChain, Naics, PyramidofPain
from ..models.control import Control, ControlCsc, ControlCscFamily, ControlDomain, ControlFamily, ControlAlertMethod, ControlFunction, ControlFeature, ControlCategory, ControlCategoryType, ControlCategoryKPO, ControlCategorySLA, DependencyEffort, OnusMethod, DeliveryMethod, BillingMethod
from ..models.entry import Register, Entry, EntryActor, EntryTask, EntryCause, EntryCompanyControl, EntryCompliance, EntryComplianceRequirement, EntryEvaluation, EntryIndicator, EntryCompanyLocation, EntryResponseSubmission, EntryRiskType, RiskType, Response, ResponseVote, EntryUrl, MitigationAdequacy
from ..models.feedback import Feedback, FeedbackStatus, FeedbackType, FeedbackQuestion, FeedbackAnswer, FeedbackCorrespondence
from ..models.meeting import Meeting, MeetingTopicComment, MeetingTopicAction, MeetingTopic, MeetingType
from ..models.scenario import EventType, FrequencyCategory, ImpactCategory, ImpactType, CIATriad, SeverityCategory
from ..models.ir import PlaybookRole, PlaybookRoleType, PlaybookActionType, PlaybookResponsibility
from ..models.vendor import Vendor, VendorType, VendorCategory
from ..models.project import Project, ProjectAssumption, ProjectSuccessCriteria, ProjectBenefit, ProjectMilestone, ProjectRisk, ProjectRiskType, ProjectBudgetChange, ProjectDateChange, ProjectUAT, ProjectUpdate


# Admin files
from .auth import UserAdmin, AccountAdmin, AccountMembership, AccountTypeAdmin, UserAccessAdmin, UserRoleAdmin, UserGrantAdmin, RoleTrackingAdmin, AuthenticationTypeAdmin
from .company import CompanyAdmin, CompanyMemberAdmin, CompanyMemberRoleAdmin, CompanyMemberRoleTypeAdmin, CompanyAssetAdmin, CompanyArtifactAdmin, CompanyObjectiveAdmin, CompanyControlAdmin, CompanyControlMeasureAdmin, CompanyControlMeasurementResultAdmin, CompanyControlCapexAdmin, CompanyControlDependencyAdmin, CompanyControlCostAdmin, CompanyControlCostTypeAdmin, CompanyContactAdmin, ContactTypeAdmin, CompanyTeamAdmin, CompanyAssetTypeAdmin, CompanyControlAdmin, CompanyLocationAdmin, CompanyFindingAdmin, CompanyPlaybookAdmin, CompanyPlaybookActionAdmin
from .actor import ActorIntentAdmin, ActorMotiveAdmin, ActorAdmin
from .audit import NotificationAdmin, NotificationGroupAdmin, AuditChangeAdmin, SnapshotAdmin
from .common import CalendarAdmin, CurrencyTypeAdmin, RAGIndicatorAdmin, EmailTemplateAdmin, ExpressionAdmin, IntegerTypeAdmin, CadenceAdmin, TimeUnitAdmin, TaskStatusAdmin, JobTitleAdmin, AppetiteAdmin
from .compliance import ComplianceAdmin, ComplianceTypeAdmin, ComplianceVersionAdmin, ComplianceRequirementAdmin, KillChainAdmin, NaicsAdmin, PyramidofPainAdmin
from .control import ControlAdmin, ControlCscAdmin, ControlCscFamilyAdmin, ControlDomainAdmin, ControlFamilyAdmin, ControlAlertMethodAdmin, ControlFunctionAdmin, ControlFeatureAdmin, ControlCategoryAdmin, ControlCategoryTypeAdmin, ControlCategoryKPOAdmin, ControlCategorySLAAdmin, DependencyEffortAdmin, OnusMethodAdmin, DeliveryMethodAdmin, BillingMethodAdmin
from .entry import RegisterAdmin, EntryAdmin, EntryActorAdmin, EntryTaskAdmin, EntryCauseAdmin, EntryCompanyControlAdmin, EntryComplianceAdmin, EntryComplianceRequirementAdmin, EntryEvaluationAdmin, EntryIndicatorAdmin, EntryCompanyLocationAdmin, EntryResponseSubmissionAdmin, ResponseAdmin, ResponseVoteAdmin, EntryUrlAdmin, RiskTypeAdmin, MitigationAdequacyAdmin
from .feedback import FeedbackAdmin, FeedbackStatusAdmin, FeedbackTypeAdmin, FeedbackQuestionAdmin, FeedbackAnswerAdmin, FeedbackCorrespondenceAdmin
from .meeting import MeetingAdmin, MeetingTopicCommentAdmin, MeetingTopicActionAdmin, MeetingTopicAdmin, MeetingTypeAdmin
from .scenario import EventTypeAdmin, FrequencyCategoryAdmin, ImpactCategoryAdmin, ImpactTypeAdmin, CIATriadAdmin, SeverityCategoryAdmin
from .ir import PlaybookRoleAdmin, PlaybookRoleTypeAdmin, PlaybookActionTypeAdmin, PlaybookResponsibilityAdmin
from .vendor import VendorAdmin, VendorTypeAdmin, VendorCategoryAdmin
from .project import ProjectAdmin, ProjectAssumptionAdmin, ProjectSuccessCriteriaAdmin, ProjectBenefitAdmin, ProjectMilestoneAdmin, ProjectRiskAdmin, ProjectRiskTypeAdmin, ProjectBudgetChangeAdmin, ProjectDateChangeAdmin, ProjectUATAdmin, ProjectUpdateAdmin
# Register your models here.

admin.site.register(ActorIntent, ActorIntentAdmin)
admin.site.register(ActorMotive, ActorMotiveAdmin)
admin.site.register(Actor, ActorAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(NotificationGroup, NotificationGroupAdmin)
admin.site.register(AuditChange, AuditChangeAdmin)
admin.site.register(Snapshot, SnapshotAdmin)
admin.site.register(User, UserAdmin)
#admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(AuthenticationType, AuthenticationTypeAdmin)
admin.site.register(AccountType, AccountTypeAdmin)
admin.site.register(UserAccess, UserAccessAdmin)
admin.site.register(UserRole, UserRoleAdmin)
admin.site.register(UserGrant, UserGrantAdmin)
admin.site.register(RoleTracking, RoleTrackingAdmin)
admin.site.register(Calendar, CalendarAdmin)
admin.site.register(CurrencyType, CurrencyTypeAdmin)
admin.site.register(RAGIndicator, RAGIndicatorAdmin)
admin.site.register(EmailTemplate, EmailTemplateAdmin)
admin.site.register(Expression, ExpressionAdmin)
admin.site.register(IntegerType, IntegerTypeAdmin)
admin.site.register(Cadence, CadenceAdmin)
admin.site.register(TimeUnit, TimeUnitAdmin)
admin.site.register(TaskStatus, TaskStatusAdmin)
admin.site.register(JobTitle, JobTitleAdmin)
admin.site.register(Appetite, AppetiteAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(CompanyMember, CompanyMemberAdmin)
admin.site.register(CompanyMemberRole, CompanyMemberRoleAdmin)
admin.site.register(CompanyMemberRoleType, CompanyMemberRoleTypeAdmin)
admin.site.register(CompanyObjective, CompanyObjectiveAdmin)
admin.site.register(CompanyLocation, CompanyLocationAdmin)
admin.site.register(CompanyArtifact, CompanyArtifactAdmin)
admin.site.register(CompanyAsset, CompanyAssetAdmin)
admin.site.register(CompanyAssetType, CompanyAssetTypeAdmin)
admin.site.register(CompanyControl, CompanyControlAdmin)
admin.site.register(CompanyControlMeasure, CompanyControlMeasureAdmin)
admin.site.register(CompanyControlMeasurementResult,
                    CompanyControlMeasurementResultAdmin)
admin.site.register(CompanyControlCapex, CompanyControlCapexAdmin)
admin.site.register(CompanyControlCost, CompanyControlCostAdmin)
admin.site.register(CompanyControlCostType, CompanyControlCostTypeAdmin)
admin.site.register(CompanyPlaybook, CompanyPlaybookAdmin)
admin.site.register(CompanyPlaybookAction, CompanyPlaybookActionAdmin)
admin.site.register(CompanyContact, CompanyContactAdmin)
admin.site.register(CompanyFinding, CompanyFindingAdmin)
admin.site.register(ContactType, ContactTypeAdmin)
admin.site.register(CompanyTeam, CompanyTeamAdmin)
admin.site.register(Compliance, ComplianceAdmin)
admin.site.register(ComplianceType, ComplianceTypeAdmin)
admin.site.register(ComplianceRequirement, ComplianceRequirementAdmin)
admin.site.register(ComplianceVersion, ComplianceVersionAdmin)
admin.site.register(KillChain, KillChainAdmin)
admin.site.register(Naics, NaicsAdmin)
admin.site.register(PyramidofPain, PyramidofPainAdmin)
admin.site.register(Control, ControlAdmin)
admin.site.register(ControlCsc, ControlCscAdmin)
admin.site.register(ControlCscFamily, ControlCscFamilyAdmin)
admin.site.register(ControlDomain, ControlDomainAdmin)
admin.site.register(ControlFamily, ControlFamilyAdmin)
admin.site.register(ControlAlertMethod, ControlAlertMethodAdmin)
admin.site.register(ControlFunction, ControlFunctionAdmin)
admin.site.register(ControlFeature, ControlFeatureAdmin)
admin.site.register(ControlCategory, ControlCategoryAdmin)
admin.site.register(ControlCategoryType, ControlCategoryTypeAdmin)
admin.site.register(ControlCategoryKPO, ControlCategoryKPOAdmin)
admin.site.register(ControlCategorySLA, ControlCategorySLAAdmin)
admin.site.register(DependencyEffort, DependencyEffortAdmin)
admin.site.register(OnusMethod, OnusMethodAdmin)
admin.site.register(DeliveryMethod, DeliveryMethodAdmin)
admin.site.register(BillingMethod, BillingMethodAdmin)
admin.site.register(Register, RegisterAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(EntryActor, EntryActorAdmin)
admin.site.register(EntryTask, EntryTaskAdmin)
admin.site.register(EntryCause, EntryCauseAdmin)
admin.site.register(EntryCompanyControl, EntryCompanyControlAdmin)
admin.site.register(EntryCompliance, EntryComplianceAdmin)
admin.site.register(EntryComplianceRequirement,
                    EntryComplianceRequirementAdmin)
admin.site.register(EntryEvaluation, EntryEvaluationAdmin)
#admin.site.register(EntryImpact, EntryImpactAdmin)
admin.site.register(EntryIndicator, EntryIndicatorAdmin)
admin.site.register(EntryCompanyLocation, EntryCompanyLocationAdmin)
admin.site.register(EntryResponseSubmission, EntryResponseSubmissionAdmin)
#admin.site.register(EntryRiskType, EntryRiskTypeAdmin)
admin.site.register(RiskType, RiskTypeAdmin)
admin.site.register(ResponseVote, ResponseVoteAdmin)
admin.site.register(Response, ResponseAdmin)
admin.site.register(EntryUrl, EntryUrlAdmin)
admin.site.register(MitigationAdequacy, MitigationAdequacyAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(FeedbackQuestion, FeedbackQuestionAdmin)
admin.site.register(FeedbackAnswer, FeedbackAnswerAdmin)
admin.site.register(FeedbackCorrespondence, FeedbackCorrespondenceAdmin)
admin.site.register(FeedbackStatus, FeedbackStatusAdmin)
admin.site.register(FeedbackType, FeedbackTypeAdmin)
admin.site.register(Meeting, MeetingAdmin)
admin.site.register(MeetingTopicComment, MeetingTopicCommentAdmin)
admin.site.register(MeetingTopicAction, MeetingTopicActionAdmin)
admin.site.register(MeetingTopic, MeetingTopicAdmin)
admin.site.register(MeetingType, MeetingTypeAdmin)
admin.site.register(EventType, EventTypeAdmin)
admin.site.register(FrequencyCategory, FrequencyCategoryAdmin)
admin.site.register(ImpactCategory, ImpactCategoryAdmin)
admin.site.register(ImpactType, ImpactTypeAdmin)
admin.site.register(CIATriad, CIATriadAdmin)
admin.site.register(SeverityCategory, SeverityCategoryAdmin)
admin.site.register(PlaybookRoleType, PlaybookRoleTypeAdmin)
admin.site.register(PlaybookRole, PlaybookRoleAdmin)
admin.site.register(PlaybookActionType, PlaybookActionTypeAdmin)
admin.site.register(PlaybookResponsibility, PlaybookResponsibilityAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(VendorType, VendorTypeAdmin)
admin.site.register(VendorCategory, VendorCategoryAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectAssumption, ProjectAssumptionAdmin)
admin.site.register(ProjectSuccessCriteria, ProjectSuccessCriteriaAdmin)
admin.site.register(ProjectBenefit, ProjectBenefitAdmin)
admin.site.register(ProjectMilestone, ProjectMilestoneAdmin)
admin.site.register(ProjectRisk, ProjectRiskAdmin)
admin.site.register(ProjectRiskType, ProjectRiskTypeAdmin)
admin.site.register(ProjectBudgetChange, ProjectBudgetChangeAdmin)
admin.site.register(ProjectDateChange, ProjectDateChangeAdmin)
admin.site.register(ProjectUAT, ProjectUATAdmin)
admin.site.register(ProjectUpdate, ProjectUpdateAdmin)
admin.site.unregister(Group)
