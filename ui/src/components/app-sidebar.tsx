import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";
import { useTheme } from "next-themes";
import { Sun, Moon, MessageSquare, FileText } from "lucide-react";

export function AppSidebar() {
  const { theme, setTheme } = useTheme();
  const [uploadedFiles, setUploadedFiles] = useState<string[]>([]);

  useEffect(() => {
    // Example: you can replace this with API call
    const storedFiles = JSON.parse(
      localStorage.getItem("uploadedFiles") || "[]",
    );
    setUploadedFiles(storedFiles);
  }, []);

  return (
    <Sidebar>
      <SidebarContent>
        {/* === Main Navigation === */}
        <SidebarGroup>
          <SidebarGroupLabel>Teclusion</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              <SidebarMenuItem>
                <SidebarMenuButton asChild>
                  <Link to="/" className="flex items-center gap-2">
                    <MessageSquare className="w-4 h-4" />
                    <span>Chat</span>
                  </Link>
                </SidebarMenuButton>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <SidebarMenuButton asChild>
                  <Link to="/get_files" className="flex items-center gap-2">
                    <FileText className="w-4 h-4" />
                    <span>Upload Files</span>
                  </Link>
                </SidebarMenuButton>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>

        {/* === Uploaded Files Section === */}
        <SidebarGroup>
          <SidebarGroupLabel>Uploaded Files</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {uploadedFiles.length > 0 ? (
                uploadedFiles.map((file, index) => (
                  <SidebarMenuItem key={index}>
                    <SidebarMenuButton asChild>
                      <button className="flex items-center gap-2 text-left">
                        <FileText className="w-4 h-4" />
                        <span>{file}</span>
                      </button>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                ))
              ) : (
                <p className="text-sm text-muted-foreground px-3">
                  No files yet
                </p>
              )}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>

      <SidebarFooter className="p-2">
        <button
          onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
          className="flex items-center justify-center w-10 h-10 border rounded-full bg-black text-white hover:bg-gray-500 dark:hover:bg-gray-800"
        >
          {theme === "dark" ? (
            <Sun className="w-5 h-5" />
          ) : (
            <Moon className="w-5 h-5" />
          )}
        </button>
      </SidebarFooter>
    </Sidebar>
  );
}
