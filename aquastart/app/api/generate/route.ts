import { execFile } from 'node:child_process';
import { promises as fs } from 'node:fs';
import path from 'node:path';
import { promisify } from 'node:util';
import { NextResponse } from 'next/server';

const execFileAsync = promisify(execFile);

async function generatePDF() {
    const repoRoot = process.cwd();
    const backendDir = path.join(repoRoot, 'backend');
    const outputPath = path.join(
        backendDir,
        'output',
        'AquaStart_Parametry.pdf'
    );

    // ReportLab PDF generation happens in the Python backend script.
    await execFileAsync('python3', ['pdf_generator.py'], { cwd: backendDir });

    const pdfBytes = await fs.readFile(outputPath);

    return new NextResponse(pdfBytes, {
        status: 200,
        headers: {
            'Content-Type': 'application/pdf',
            'Content-Disposition': 'attachment; filename="AquaStart_Parametry.pdf"',
        },
    });
}

export async function GET() {
    try {
        return await generatePDF();
    } catch (error) {
        console.error('Error generating PDF:', error);
        return NextResponse.json(
            { error: 'Failed to generate PDF' },
            { status: 500 }
        );
    }
}

export async function POST() {
    try {
        return await generatePDF();
    } catch (error) {
        console.error('Error generating PDF:', error);
        return NextResponse.json(
            { error: 'Failed to generate PDF' },
            { status: 500 }
        );
    }
}