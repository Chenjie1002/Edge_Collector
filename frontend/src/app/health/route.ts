export function GET(): Response {
  return Response.json(
    {
      status: "ok",
      service: "dashboard"
    },
    { status: 200 }
  );
}
