# -----------------------------
# TOOL DEFINITIONS
# -----------------------------
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "find_user_by_email",
            "description": "Find a user using email address",
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "User email address"
                    }
                },
                "required": ["email"]
            }
        }
    },
    # -----------------------------
    # ISSUE TOOLS
    # -----------------------------
    {
        "type": "function",
        "function": {
            "name": "create_issue_tool",
            "description": "Create a new issue under a project",
            "parameters": {
                "type": "object",
                "properties": {
                    "project_id": {
                        "type": "integer",
                        "description": "Project ID where issue will be created"
                    },
                    "title": {
                        "type": "string",
                        "description": "Issue title"
                    },
                    "description": {
                        "type": "string",
                        "description": "Detailed issue description"
                    },
                    "status": {
                        "type": "string",
                        "description": "Issue status",
                        "default": "open"
                    }
                },
                "required": ["project_id", "title", "description"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_issues_tool",
            "description": "Get all issues of a project",
            "parameters": {
                "type": "object",
                "properties": {
                    "project_id": {
                        "type": "integer"
                    },
                    "limit": {
                        "type": "integer",
                        "default": 10
                    },
                    "offset": {
                        "type": "integer",
                        "default": 0
                    }
                },
                "required": ["project_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_issue_status_tool",
            "description": "Update status of an issue",
            "parameters": {
                "type": "object",
                "properties": {
                    "issue_id": {
                        "type": "integer"
                    },
                    "status": {
                        "type": "string",
                        "description": "New status (open, in_progress, closed)"
                    }
                },
                "required": ["issue_id", "status"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "assign_issue_tool",
            "description": "Assign an issue to a user",
            "parameters": {
                "type": "object",
                "properties": {
                    "issue_id": {
                        "type": "integer"
                    },
                    "user_id": {
                        "type": "integer"
                    }
                },
                "required": ["issue_id", "user_id"]
            }
        }
    },
    # -----------------------------
    # PROJECT TOOLS
    # -----------------------------
    {
        "type": "function",
        "function": {
            "name": "create_project_tool",
            "description": "Create a new project",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "Owner user ID"
                    },
                    "name": {
                        "type": "string",
                        "description": "Project name"
                    },
                    "description": {
                        "type": "string",
                        "description": "Project description"
                    }
                },
                "required": ["user_id", "name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_project_tool",
            "description": "Update an existing project",
            "parameters": {
                "type": "object",
                "properties": {
                    "project_id": {
                        "type": "integer"
                    },
                    "data": {
                        "type": "object",
                        "description": "Fields to update (name, description etc.)"
                    }
                },
                "required": ["project_id", "data"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_project_tool",
            "description": "Delete a project",
            "parameters": {
                "type": "object",
                "properties": {
                    "project_id": {
                        "type": "integer"
                    }
                },
                "required": ["project_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_issue_with_ai_tool",
            "description": "Create an issue using natural language description. AI will generate structured title and description automatically and optionally assign it to a user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "project_id": {
                        "type": "integer"
                    },
                    "user_description": {
                        "type": "string",
                        "description": "Raw user description of the issue"
                    },
                    "assign_to": {
                        "type": "integer",
                        "description": "Optional user ID to assign issue"
                    }
                },
                "required": ["project_id", "user_description"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "find_project_by_name_tool",
            "description": "Find a project using its name and return project details including project ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Project name to search for"
                    }
                },
                "required": ["name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_project_tool",
            "description": "Get project details using project ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "project_id": {
                        "type": "integer",
                        "description": "Project ID"
                    }
                },
                "required": ["project_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_user_issues_tool_or_get_current_user_issues_tool",
            "description": "Get all issues assigned to a user or current user issues.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "User ID"
                    }
                },
                "required": ["user_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_projects_tool",
            "description": "Get all projects belonging to the current user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "current_user_id": {
                        "type": "integer",
                        "description": "User ID"
                    }
                },
                "required": ["current_user_id"]
            }
        }
    }

#********************************************************************

#     {
#         "type": "function",
#         "function": {
#             "name": "find_user_by_email",
#             "description": "Find a user by email address.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "email": {"type": "string", "description": "User email address"}
#                 },
#                 "required": ["email"],
#             },
#         },
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "get_user_tool",
#             "description": "Get user details using user ID.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "user_id": {"type": "integer", "description": "User ID"}
#                 },
#                 "required": ["user_id"],
#             },
#         },
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "get_current_user_tool",
#             "description": "Get information about the currently authenticated user.",
#             "parameters": {"type": "object", "properties": {}},
#         },
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "search_users_tool",
#             "description": "Search users by email using ilike.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {"query": {"type": "string"}},
#                 "required": ["query"],
#             },
#         },
#     },
]
