// app/favicon/route.js
import { ImageResponse } from 'next/server';

export async function GET() {
  return new ImageResponse(
    (
      <div
        style={{
          fontSize: 40,
          color: 'black',
          background: 'white',
          width: '100%',
          height: '100%',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          borderRadius: '50%',
        }}
      >
        T
      </div>
    ),
    {
      width: 32,
      height: 32,
    }
  );
}