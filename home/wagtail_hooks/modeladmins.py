from wagtail.core import hooks
from .models import (
    Attendance,
    Absentee,
    BlogPostPage,
    Collaborators,
    Course,
    HomePage,
    AttendanceIssue,
    AskForLeaveMember,
    Article,
    Symposium,
    Webinar,
    ResearchPaper,
    Project,
    Notification,
    Gallery
)

from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    modeladmin_register,
    ModelAdminGroup,
)

class ArticleAdmin(ModelAdmin):
    model = Article
    menu_label = "Articles"
    menu_icon = "doc-full"
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("title", "date_published", "live")
    list_filter = ("live", "date_published", "owner")
    search_fields = ("title", "date_published", "content", "owner")


class ResearchPaperAdmin(ModelAdmin):
    model = ResearchPaper
    menu_label = "Research Paper"
    menu_icon = "doc-full"
    menu_order = 500
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("title", "author")
    list_filter = ("author",)
    search_fields = ("title", "author")


class PublicationsAdminGroup(ModelAdminGroup):
    menu_icon = "folder-inverse"
    menu_label = "Publications"
    menu_order = 700
    items = (
        ResearchPaperAdmin,
        ArticleAdmin,
    )


modeladmin_register(PublicationsAdminGroup)


class AttendanceAdmin(ModelAdmin):
    model = Attendance
    menu_label = "Attendance Sheet"
    menu_icon = "doc-full"
    menu_order = 300
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("issue_date", "member", "status")
    list_filter = ("issue_date", "status", "member")
    search_fields = ("member", "remarks")


class AttendanceIssueAdmin(ModelAdmin):
    model = AttendanceIssue
    menu_label = "Issue Attendance"
    menu_icon = "doc-full"
    menu_order = 400
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("date",)
    list_filter = ("date",)
    search_fields = ("date", "remarks")
    inspect_view_enabled = True
    inspect_view_class = AttendanceIssueInspect
    inspect_view_fields = [
        "date",
        "remarks",
        "is_open",
    ]


class AbsenteeListAdmin(ModelAdmin):
    model = Absentee
    menu_label = "Absentees"
    menu_icon = "doc-full"
    menu_order = 500
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("issue_date", "member")
    list_filter = ("issue_date", "member")
    search_fields = ("issue_date", "member", "remarks")


class AskForLeaveMemberAdmin(ModelAdmin):
    model = AskForLeaveMember
    menu_label = "Leave Applications"
    menu_icon = "doc-full"
    menu_order = 500
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("leave_start_date", "leave_end_date", "member", "is_approved")
    list_filter = ("member", "is_approved")
    search_fields = ("member", "remarks")


class AttendanceAdminGroup(ModelAdminGroup):
    menu_icon = "folder-inverse"
    menu_label = "Attendance"
    menu_order = 700
    items = (
        AttendanceAdmin,
        AttendanceIssueAdmin,
        AbsenteeListAdmin,
        AskForLeaveMemberAdmin,
    )


modeladmin_register(AttendanceAdminGroup)


class WebinarAdmin(ModelAdmin):
    model = Webinar
    menu_label = "Webinar"
    menu_icon = "pilcrow"
    list_display = ("title", "program_date")
    list_filter = ("date_added",)
    search_fields = ("title", "description")


class SymposiumAdmin(ModelAdmin):
    model = Symposium
    menu_label = "Symposium"
    menu_icon = "pilcrow"
    list_display = ("title", "date")
    list_filter = ("date_added",)
    search_fields = ("title", "description")


class ProgramsAdminGroup(ModelAdminGroup):
    menu_icon = "folder-inverse"
    menu_label = "Programs"
    menu_order = 700
    items = (WebinarAdmin, SymposiumAdmin)


modeladmin_register(ProgramsAdminGroup)


class ProjectAdmin(ModelAdmin):
    model = Project
    menu_icon = "folder-inverse"
    menu_label = "Projects"
    menu_order = 700
    list_display = ("title", "start_date", "end_date")
    search_fields = ("title", "overview", "description")
    list_filter = ("members",)


modeladmin_register(ProjectAdmin)


class CollaboratorsAdmin(ModelAdmin):
    model = Collaborators
    menu_icon = "folder-inverse"
    menu_label = "Collaborators"
    menu_order = 700

modeladmin_register(CollaboratorsAdmin)

class CourseAdmin(ModelAdmin):
    model = Course
    menu_icon = "folder-inverse"
    menu_label = "Courses"
    menu_order = 700
    list_display = (
        "title",
        "date",
    )
    search_fields = ("title", "date", "description")


modeladmin_register(CourseAdmin)

class BlogAdmin(ModelAdmin):
    model = BlogPostPage
    menu_icon = "folder-inverse"
    menu_label = "Blogs"
    menu_order = 700
    list_display = (
        "title",
    )
    search_fields = ("title", "content")


modeladmin_register(BlogAdmin)
class GalleryAdmin(ModelAdmin):
    model = Gallery
    menu_icon = "folder-inverse"
    menu_label = "Gallery"
    menu_order = 700
    list_display = (
        "thumbnail",
    )

modeladmin_register(GalleryAdmin)
