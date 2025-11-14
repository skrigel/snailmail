import { cn } from "@/lib/utils";
import type { SVGProps } from "react";

const SnailMailIcon = (props: SVGProps<SVGSVGElement>) => (
  <div>
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 16 16"
    shapeRendering="crispEdges"
    className={cn("pixelated", props.className)}
    {...props}
  >
    <g fill="hsl(var(--foreground))">
      <path d="M6 10h1v1H6zM9 10h1v1H9z" />
    </g>
    <g fill="hsl(var(--primary))">
      <path d="M3 4h1v1H3zM4 3h1v1H4zM5 2h5v1H5zM10 3h1v1h-1zM11 4h1v1h-1zM12 5h1v5h-1zM11 10h1v1h-1zM10 11h1v1h-1zM5 12h5v1H5zM4 11h1v1H4zM3 10h1v1H3zM2 5h1v5H2z" />
    </g>
    <g fill="hsl(var(--accent))">
      <path d="M4 5h1v1H4zM5 4h1v1H5zM6 3h1v1H6zM7 3h1v1H7zM8 3h1v1H8zM9 4h1v1H9zM10 5h1v1h-1zM11 6h1v1h-1zM11 7h1v1h-1zM11 8h1v1h-1zM11 9h1v1h-1zM10 10h1v1h-1zM9 11h1v1H9zM8 11h1v1H8zM7 11h1v1H7zM6 11h1v1H6zM5 10h1v1H5zM4 9h1v1H4zM4 8h1v1H4zM4 7h1v1H4zM4 6h1v1H4z" />
    </g>
    <g fill="hsl(var(--card-foreground))">
      <path d="M0 13h16v1H0z" />
      <path d="M0 14h2v1H0zM3 14h2v1H3zM6 14h1v1H6zM8 14h2v1H8zM11 14h1v1h-1zM13 14h3v1h-3z" />
    </g>
  </svg>
  </div>

);

export default SnailMailIcon;
