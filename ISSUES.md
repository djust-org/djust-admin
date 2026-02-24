# djust-admin Issues and Missing Functionality

This document tracks known issues and missing functionality in djust-admin.

## High Priority

### 1. ForeignKey and ManyToMany Field Support
**Status:** Not implemented

Currently, ForeignKey and ManyToMany fields render as text inputs instead of select/multi-select widgets. Need to:
- Detect ForeignKey fields and render as dropdown selects
- Detect ManyToMany fields and render as multi-select or dual-list widgets
- Implement autocomplete for large datasets
- Handle related object creation inline (add popup)

**Files affected:**
- `djust_admin/views.py` - `get_context_data()` in `ModelDetailView`
- `djust_admin/templates/djust_admin/model_detail.html`

### 2. Date/Time Field Widgets
**Status:** Not implemented

Date, DateTime, and Time fields render as text inputs instead of proper date/time pickers.

**Solution options:**
- Use HTML5 date/datetime-local/time inputs
- Integrate a JavaScript date picker library (flatpickr, etc.)
- Create custom djust components for date/time selection

### 3. List View Filtering
**Status:** Not implemented

The `list_filter` configuration is defined in model admins but not rendered in the list view.

**Needs:**
- Sidebar filter panel
- Filter by choice fields
- Filter by date ranges
- Filter by related objects (ForeignKey)

## Medium Priority

### 4. Authentication and Authorization
**Status:** Not implemented

Currently, the admin is accessible without authentication.

**Needs:**
- Login view
- Logout functionality
- Permission checking (view, add, change, delete)
- Staff-only access enforcement

### 5. Bulk Actions
**Status:** Partially implemented

The `delete_selected` action is defined but the UI for bulk actions needs work.

**Needs:**
- Action dropdown when items are selected
- Confirmation dialog for destructive actions
- Progress feedback for long-running actions

### 6. Save and Navigation
**Status:** Partially implemented

Save buttons exist but navigation after save needs work.

**Needs:**
- Redirect to list view after successful save
- "Save and add another" should clear form and stay on add page
- "Save and continue editing" should stay on same object
- Show success/error messages

### 7. Delete Confirmation
**Status:** Basic implementation

Delete view exists but needs:
- Show related objects that will be deleted (cascade preview)
- Confirm deletion and redirect to list

## Low Priority

### 8. Inline Editing
**Status:** Not implemented

Support for editing related objects inline (like Django admin's TabularInline, StackedInline).

### 9. Search Highlighting
**Status:** Not implemented

When searching, highlight the matching text in results.

### 10. Sortable Columns
**Status:** Partially implemented

Column headers are clickable but sorting indicator could be improved.

### 11. Custom Actions
**Status:** Not implemented

Support for custom admin actions beyond delete_selected.

### 12. Field-level Help Text
**Status:** Implemented

Help text from model fields is displayed below form inputs.

### 13. Readonly Fields
**Status:** Implemented

Readonly fields are displayed as text instead of inputs.

## Rust Template Engine Limitations

### Custom Template Filters
The djust Rust template engine doesn't support Django's `{% load %}` tag for custom template filters. Workaround is to pre-compute data in Python views instead of using dynamic filters in templates.

**Affected patterns:**
- `{{ form|get_field:field_name }}` - Must pre-compute field data in view
- `{{ dict|get_item:key }}` - Must pre-compute values in view

**Solution:** Pre-compute all dynamic lookups in `get_context_data()` and pass flat, serializable data to templates.

---

## Completed

- [x] Dashboard/index page with app/model listing
- [x] Model list view with pagination
- [x] Search functionality
- [x] Add/Create form
- [x] Edit/Change form
- [x] Delete confirmation view
- [x] Fieldsets grouping
- [x] Required field indicators
- [x] Checkbox fields
- [x] Textarea fields
- [x] Select/choice fields
- [x] Form validation errors
- [x] Success messages
