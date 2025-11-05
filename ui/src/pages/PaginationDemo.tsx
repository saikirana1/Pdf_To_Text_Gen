import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import {
  Pagination,
  PaginationContent,
  PaginationItem,
  PaginationLink,
  PaginationPrevious,
  PaginationNext,
  PaginationEllipsis,
} from "@/components/ui/pagination";

interface Student {
  id: number;
  name: string;
}

interface PaginatedResponse {
  items: Student[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

const fetchStudents = async (page: number): Promise<PaginatedResponse> => {
  const res = await axios.get(
    `http://127.0.0.1:8000/students?page=${page}&size=5`
  );
  return res.data;
};

export function PaginationDemo() {
  const [page, setPage] = useState(1);

  const { data, isLoading, isError } = useQuery({
    queryKey: ["students", page],
    queryFn: () => fetchStudents(page),
  });

  if (isLoading) return <p className="text-center mt-10">Loading...</p>;
  if (isError)
    return (
      <p className="text-center mt-10 text-red-500">Failed to load data</p>
    );

  const totalPages = data?.pages || 1;

  return (
    <div className="flex flex-col items-center p-4">
      <h1 className="text-xl font-semibold mb-4">Students List</h1>

      <ul className="w-full max-w-md bg-white rounded-lg shadow-md p-4">
        {data?.items.map((student) => (
          <li key={student.id} className="border-b py-2 px-3 hover:bg-gray-50">
            {student.name}
          </li>
        ))}
      </ul>

      <Pagination className="mt-6">
        <PaginationContent>
          {/* 🔸 PREVIOUS BUTTON */}
          <PaginationItem>
            <PaginationPrevious
              href="#"
              onClick={() => setPage((p) => Math.max(p - 1, 1))}
              className={`${
                page === 1
                  ? "pointer-events-none opacity-50 cursor-not-allowed"
                  : ""
              }`}
            />
          </PaginationItem>

          {/* 🔸 PAGE NUMBERS */}
          {[...Array(totalPages)].map((_, i) => (
            <PaginationItem key={i}>
              <PaginationLink
                href="#"
                isActive={page === i + 1}
                onClick={() => setPage(i + 1)}
              >
                {i + 1}
              </PaginationLink>
            </PaginationItem>
          ))}

          {totalPages > 5 && <PaginationEllipsis />}

          {/* 🔸 NEXT BUTTON */}
          <PaginationItem>
            <PaginationNext
              href="#"
              onClick={() => setPage((p) => Math.min(p + 1, totalPages))}
              className={`${
                page === totalPages
                  ? "pointer-events-none opacity-50 cursor-not-allowed"
                  : ""
              }`}
            />
          </PaginationItem>
        </PaginationContent>
      </Pagination>
    </div>
  );
}
